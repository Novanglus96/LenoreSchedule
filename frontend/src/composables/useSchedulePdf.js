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

function calcHours(startTime, endTime) {
  if (!startTime || !endTime) return null;
  const [sh, sm] = startTime.split(":").map(Number);
  const [eh, em] = endTime.split(":").map(Number);
  const totalMinutes = eh * 60 + em - (sh * 60 + sm);
  if (totalMinutes <= 0) return null;
  const h = Math.floor(totalMinutes / 60);
  const m = totalMinutes % 60;
  return m === 0 ? `${h}h` : `${h}h${m}m`;
}

function entryText(entry) {
  if (entry.source === "holiday") return entry.holiday_name || "Holiday";
  if (entry.entry_type === "day_off") return "Day Off";
  if (entry.start_time && entry.end_time) {
    const hours = calcHours(entry.start_time, entry.end_time);
    const timeStr = `${fmtTime(entry.start_time)}-${fmtTime(entry.end_time)}`;
    const base = hours ? `${timeStr} (${hours})` : timeStr;
    if (entry.source === "calendar") {
      return base + (entry.confirmed ? " ✓" : " ?");
    }
    return base;
  }
  const label = entry.entry_type.replace(/_/g, " ");
  if (entry.source === "calendar") {
    return label + (entry.confirmed ? " ✓" : " ?");
  }
  return label;
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
  doc.text(`Pay Period: ${year} #${page + 1}`, margin + 8, top + 30);
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
  function downloadPdf(schedule, year, page) {
    if (!schedule) return;

    const doc = new jsPDF({ orientation: "landscape", unit: "pt", format: "letter" });
    const pageWidth = doc.internal.pageSize.getWidth();

    const tableStartY = drawHeader(doc, schedule, year, page);

    // Build day column headers from first available employee
    let dayDates = [];
    for (const div of schedule.divisions) {
      if (div.employees.length && div.employees[0].days.length) {
        dayDates = div.employees[0].days.map((d) => d.date);
        break;
      }
    }

    const head = [["Employee", ...dayDates.map(dayHeader)]];

    const body = [];
    for (const div of schedule.divisions) {
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

      for (const emp of div.employees) {
        const row = [`${emp.last_name}, ${emp.first_name}`];
        for (const day of emp.days) {
          row.push(day.entries.length === 0 ? "—" : day.entries.map(entryText).join("\n"));
        }
        body.push(row);
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

    const safeName = `${year}-pay-period-${page + 1}`;
    doc.save(`schedule-${safeName}.pdf`);
  }

  return { downloadPdf };
}
