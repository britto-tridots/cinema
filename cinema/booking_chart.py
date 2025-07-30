import frappe
from datetime import datetime

@frappe.whitelist()
def get_booking_chart_data():
    bookings = frappe.db.sql("""
        SELECT
            s.movie,
            s.show_date,
            s.show_time,
            SUM(LENGTH(b.seat_numbers) - LENGTH(REPLACE(b.seat_numbers, ',', '')) + 1) AS total
        FROM `tabBooking` b
        JOIN `tabShowtime` s ON b.showtime = s.name
        WHERE b.status = 'Booked'
        GROUP BY s.movie, s.show_date, s.show_time
        ORDER BY s.show_date, s.show_time
    """, as_dict=True)

    def format_label(row):
    # Handle string time like "05:00 PM"
        if isinstance(row['show_time'], str):
            show_time = datetime.strptime(row['show_time'], "%I:%M %p").time()
        else:
            show_time = row['show_time']
        
        dt = datetime.combine(row['show_date'], show_time)
        return dt.strftime("%d-%m-%Y %I:%M %p")

    all_labels = sorted(
        {format_label(row) for row in bookings},
        key=lambda x: datetime.strptime(x, "%d-%m-%Y %I:%M %p")
    )

    chart_data = {}
    for row in bookings:
        movie = row["movie"]
        label = format_label(row)

        if movie not in chart_data:
            chart_data[movie] = [0] * len(all_labels)

        index = all_labels.index(label)
        chart_data[movie][index] = row["total"]

    return {
        "labels": all_labels,
        "datasets": [
            {"name": movie, "values": values}
            for movie, values in chart_data.items()
        ]
    }


def after_insert(doc, method):
    frappe.publish_realtime("booking_chart_update", {"msg": "refresh"})


# def get_booking_chart_data():
#     bookings = frappe.db.sql("""
#         SELECT
#             s.movie,
#             DATE_FORMAT(s.show_date, '%d-%m-%Y') AS date,
#             TIME_FORMAT(s.show_time, '%I:%i %p') AS time,
#             SUM(LENGTH(b.seat_numbers) - LENGTH(REPLACE(b.seat_numbers, ',', '')) + 1) AS total
#         FROM `tabBooking` b
#         JOIN `tabShowtime` s ON b.showtime = s.name
#         WHERE b.status = 'Booked'
#         GROUP BY s.movie, s.show_date, s.show_time
#         ORDER BY s.show_date, s.show_time
#     """, as_dict=True)

#     print('All Bookings', bookings)

#     all_labels = sorted(
#         {f"{row['date']} {row['time']}" for row in bookings},
#         key=lambda dt: datetime.strptime(dt, "%d-%m-%Y %I:%M %p")
#     )
#     print('All Showtimes for the movie',all_labels)

#     chart_data = {}
#     for row in bookings:
#         movie = row["movie"]
#         label = f"{row['date']} {row['time']}"
#         print(chart_data)

#         if movie not in chart_data:
#             chart_data[movie] = [0] * len(all_labels)

#         index = all_labels.index(label)
#         print('index', index)
#         chart_data[movie][index] = row["total"]
#         print(chart_data)
#     return {
#         "labels": all_labels,
#         "datasets": [
#             {"name": movie, "values": values}
#             for movie, values in chart_data.items()
#         ]
#     }


