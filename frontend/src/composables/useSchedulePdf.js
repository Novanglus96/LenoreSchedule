import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

const WEEKDAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

function fmtTime(t) {
  if (!t) return "";
  const [h, m] = t.split(":");
  const hour = parseInt(h);
  const ampm = hour >= 12 ? "pm" : "am";
  return `${hour % 12 || 12}:${m}${ampm}`;
}

function calcHours(startTime, endTime, breakMinutes = 0) {
  if (!startTime || !endTime) return null;
  const [sh, sm] = startTime.split(":").map(Number);
  const [eh, em] = endTime.split(":").map(Number);
  const totalMinutes = eh * 60 + em - (sh * 60 + sm) - breakMinutes;
  if (totalMinutes <= 0) return null;
  const h = Math.floor(totalMinutes / 60);
  const m = totalMinutes % 60;
  return m === 0 ? `${h}h` : `${h}h${m}m`;
}

function entryText(entry) {
  if (entry.source === "holiday") return entry.holiday_name || "Holiday";

  let text;
  if (entry.start_time && entry.end_time) {
    const hours = calcHours(entry.start_time, entry.end_time, entry.break_minutes || 0);
    const timeStr = `${fmtTime(entry.start_time)}-${fmtTime(entry.end_time)}`;
    const base = hours ? `${timeStr} (${hours})` : timeStr;
    text = entry.entry_type ? `${base} · ${entry.entry_type}` : base;
  } else {
    text = entry.entry_type || "";
  }

  if (entry.source === "calendar") {
    text += entry.confirmed ? " ✓" : " ?";
    if (entry.notes) text += `\n${entry.notes}`;
  }

  return text;
}

function dayHeader(isoDate) {
  const dt = new Date(isoDate + "T00:00:00");
  return `${WEEKDAYS[dt.getDay()]}\n${dt.getMonth() + 1}/${dt.getDate()}`;
}

function fmtDateRange(weekStart, weekEnd) {
  const fmt = (iso) => {
    const dt = new Date(iso + "T00:00:00");
    return dt.toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" });
  };
  return `${fmt(weekStart)} – ${fmt(weekEnd)}`;
}

// Draws the page header box. Returns the Y coordinate where the table should start.
function drawHeader(doc, schedule, year, page) {
  const pageWidth = doc.internal.pageSize.getWidth();
  const margin = 36;
  const headerHeight = 54;
  const top = 20;

  // Outer border
  doc.setDrawColor(180, 180, 180);
  doc.setLineWidth(0.5);
  doc.rect(margin, top, pageWidth - margin * 2, headerHeight);

  // Left block — title + pay period
  doc.setFont("helvetica", "bold");
  doc.setFontSize(13);
  doc.setTextColor(40, 40, 40);
  doc.text("Weekly Schedule", margin + 8, top + 16);

  doc.setFont("helvetica", "normal");
  doc.setFontSize(9);
  doc.setTextColor(80, 80, 80);
  const labelFirst = schedule.week_label?.split(".")?.[0] ?? String(page + 1);
  const payNum = isNaN(Number(labelFirst)) ? page + 1 : Number(labelFirst);
  doc.text(`Pay Period: ${year} #${payNum}`, margin + 8, top + 30);
  doc.text(fmtDateRange(schedule.week_start, schedule.week_end), margin + 8, top + 42);

  // Vertical divider after left block
  const divX = margin + 160;
  doc.setDrawColor(200, 200, 200);
  doc.line(divX, top, divX, top + headerHeight);

  // Right area — reserved for future additions (notes, signatures, etc.)
  doc.setFont("helvetica", "italic");
  doc.setFontSize(7);
  doc.setTextColor(160, 160, 160);
  doc.text("Notes / Approvals", divX + 8, top + 12);

  // Reset text color
  doc.setTextColor(0, 0, 0);

  return top + headerHeight + 8;
}

export function useSchedulePdf() {
  function downloadPdf(schedule, year, page, divisionId = null) {
    if (!schedule) return;

    const divisions = divisionId
      ? schedule.divisions.filter((d) => d.division_id === divisionId)
      : schedule.divisions;

    const doc = new jsPDF({ orientation: "landscape", unit: "pt", format: "letter" });
    const pageWidth = doc.internal.pageSize.getWidth();

    const tableStartY = drawHeader(doc, schedule, year, page);

    // Build day column headers from the first available employee across filtered divisions
    let dayDates = [];
    outer: for (const div of divisions) {
      for (const grp of div.groups) {
        if (grp.employees.length && grp.employees[0].days.length) {
          dayDates = grp.employees[0].days.map((d) => d.date);
          break outer;
        }
      }
    }

    const head = [["Employee", ...dayDates.map(dayHeader)]];

    const body = [];
    for (const div of divisions) {
      // Omit the division header row when exporting a single division
      if (!divisionId) {
        body.push([
          {
            content: div.division_name,
            colSpan: 1 + dayDates.length,
            styles: {
              fontStyle: "bold",
              fillColor: [230, 230, 230],
              textColor: [50, 50, 50],
            },
          },
        ]);
      }

      for (const grp of div.groups) {
        body.push([
          {
            content: grp.group_name,
            colSpan: 1 + dayDates.length,
            styles: {
              fontStyle: "italic",
              fillColor: [245, 245, 245],
              textColor: [100, 100, 100],
              fontSize: 6,
            },
          },
        ]);

        for (const emp of grp.employees) {
          const row = [`${emp.last_name}, ${emp.first_name}`];
          for (const day of emp.days) {
            row.push(day.entries.length === 0 ? "—" : day.entries.map(entryText).join("\n"));
          }
          body.push(row);
        }
      }
    }

    autoTable(doc, {
      head,
      body,
      startY: tableStartY,
      styles: {
        fontSize: 7,
        cellPadding: 3,
        valign: "middle",
        halign: "center",
        overflow: "linebreak",
      },
      headStyles: {
        fillColor: [66, 66, 66],
        textColor: 255,
        fontStyle: "bold",
        halign: "center",
      },
      columnStyles: {
        0: { halign: "left", fontStyle: "bold", cellWidth: 80 },
      },
      alternateRowStyles: { fillColor: [248, 248, 248] },
    });

    // Footer with generation timestamp on every page
    const pageCount = doc.internal.getNumberOfPages();
    doc.setFontSize(7);
    doc.setFont("helvetica", "normal");
    for (let i = 1; i <= pageCount; i++) {
      doc.setPage(i);
      doc.text(
        `Generated ${new Date().toLocaleString()}`,
        pageWidth / 2,
        doc.internal.pageSize.getHeight() - 10,
        { align: "center" },
      );
    }

    const labelSegments = (schedule.week_label ?? "").split(".");
    const payNum =
      labelSegments.length >= 2 && !isNaN(Number(labelSegments[0]))
        ? Number(labelSegments[0])
        : page + 1;
    const weekSuffix =
      labelSegments.length >= 3 && !isNaN(Number(labelSegments[1]))
        ? `-wk${labelSegments[1]}`
        : "";
    const divisionSlug = divisionId
      ? `-${divisions[0]?.division_name.replace(/[^a-z0-9]+/gi, "-").toLowerCase() ?? "division"}`
      : "";
    doc.save(`schedule-${year}-pay-period-${payNum}${weekSuffix}${divisionSlug}.pdf`);
  }

  return { downloadPdf };
}
