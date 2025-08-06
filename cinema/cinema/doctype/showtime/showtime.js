// Copyright (c) 2025, Brit and contributors
// For license information, please see license.txt

frappe.ui.form.on('Showtime', {
    refresh: function (frm) {
        if (frm.doc.theatre) {
            frappe.db.get_doc("Theatre", frm.doc.theatre).then(doc => {
                const screens = (doc.screen || []).map(row => row.screen_name);
                frm.set_df_property("screen", "options", screens.join("\n"));
                frm.refresh_field("screen");
            });
        }
    },
    screen: function (frm) {
        if (frm.doc.theatre && frm.doc.screen) {
            frappe.call({
                method: "cinema.cinema.doctype.showtime.showtime.get_screen_capacity",
                args: {
                    theatre: frm.doc.theatre,
                    screen_name: frm.doc.screen
                },
                callback: function (r) {
                    if (r.message) {
                        frm.set_value("seats_available", r.message);
                    }
                }
            });
        }
    },

    theatre: function (frm) {
        if (frm.doc.theatre) {
            frappe.db.get_doc("Theatre", frm.doc.theatre).then(doc => {
                const screens = (doc.screen || []).map(row => row.screen_name);
                frm.set_df_property("screen", "options", screens.join("\n"));
                frm.refresh_field("screen");
            });
        }
    }
});
