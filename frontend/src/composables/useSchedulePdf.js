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

export function useSchedulePdf() {
  function downloadPdf(schedule) {
    if (!schedule) return;

    const doc = new jsPDF({ orientation: "landscape", unit: "pt", format: "letter" });
    const pageWidth = doc.internal.pageSize.getWidth();

    // Title
    doc.setFontSize(14);
    doc.setFont("helvetica", "bold");
    doc.text(schedule.week_label, pageWidth / 2, 30, { align: "center" });

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
      // Division header row spanning all columns
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
          if (day.entries.length === 0) {
            row.push("—");
          } else {
            row.push(day.entries.map(entryText).join("\n"));
          }
        }
        body.push(row);
      }
    }

    autoTable(doc, {
      head,
      body,
      startY: 45,
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

    // Footer with generation timestamp
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

    const safeName = schedule.week_label.replace(/[^a-z0-9]+/gi, "-").toLowerCase();
    doc.save(`schedule-${safeName}.pdf`);
  }

  return { downloadPdf };
}
