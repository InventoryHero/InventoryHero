export const localizations = {
  en: {
    home: "Home",
    boxes: "Boxes",
    locations: "Locations",
    products: "Products",
    box: "Box",
    product: "Product",
    location: "Location",
    save: "Save",
    not_found: "The requested resource could not be found!",
    products_view:{
      products_in: "Products in {name}",
      starred_in: "Starred products in {name}"
    },
    add_modal: {
      select_product_placeholder: "Select product",
      box_placeholder: "Box",
      location_placeholder: "Location",
      amount_placeholder: "Amount",
      starred: "Starred",
      product_name: "Name (product)",
      location_name: "Name (location)",
      box_name: "Name (box)",
      add_success_product: "Successfully added product '{name}'",
      add_success_box: "Successfully added box '{name}'",
      add_success_room: "Successfully added location '{name}'",
      add_btn_location: "Add Location",
      add_btn_box: "Add Box",
      add_btn_product: "Add Product",
      add_new_product: "Add new product",
      no_box: "No box selected",
      no_room: "No location selected"
    },
    qr_data_modal: {

    },
    qr_reader_modal: {
      invalid_qr: "Please scan a valid IH qr code",
      title: "Scan IH QR-Code"
    },
    locations_view:{
      toasts: {
          success: {
            delete: "Location '{name}' deleted successfully"
          },
          error:{
            delete: "Location '{name}' could not be deleted"
          }
      },
    },
    boxes_overview: {
      boxes_in: "Boxes in {location}"
    },
    login_view: {
      username: "Username",
      password: "Password",
      register: "Register",
      login: "Login",
      login_invalid: "Wrong username/password",
       toasts: {
          success: {
            register: "Registration successful"
          },
          error: {
            register: {
              username_taken: "This username is already taken!",
              generic_error: "Something went wrong please try again later!"
            }
          }
       }
    },
    settings_view: {
      settings: "Settings",
      theme: "Theme",
      language: "Language"
    },
    room_detail_modal: {
      toasts:{
        success: {
          rename: "Renaming location '{old}' to '{new}' successful"
        },
        error: {
          rename: "Renaming location '{old}' failed"
        }
      },
      qr_code: "QR-Code for location '{loc}'"
    },
    product_detail_modal: {
      toasts: {
        success: {
          delete: "Product '{name}' successfully deleted",
          update: "Product '{name}' updated successfully",
          amountUpdate: "Amount of product '{name}' updated successfully"
        },
        error: {
          delete: "Error while deleting product '{name'}",
          update: "Error while updating product '{name}'",
          amountUpdate: "Error while updating product '{name}' amount"
        }
      },
      amount_below_zero: "Amount cannot be below zero!"
    },
    room_card: {

    },
    box_card: {

    },
    products_card: {
      toasts: {
        success: {
          amountUpdate: "Amount of product '{name}' updated successfully"
        },
        error: {
          amountUpdate: "Error while updating product '{name}' amount"
        }
      },
    },
    home_view: {
      last_used: "⏰ Last Used Products",
      starred_products: "⭐ Starred Products"
    },
    confirmation_modal: {
      box: "box",
      location: "location",
      delete_product_expl: "Do you want to delete the whole product (in all locations)? Then press the red button.",
      delete_product_at_loc_expl: "Do you want to delete the products at location '{loc}'? Then press the yellow button",
      delete_product_at_box_expl: "Do you want to delete the products at box '{box}'? Then press the yellow button",
      delete_product_at_def_expl: "Do you want to delete the products w/o location/box? Then press the yellow button",
      delete: "Delete",
      delete_box: "Delete box",
      delete_location: "Delete location",
      delete_product: "All",
      delete_product_at_loc: "This",
      delete_storage: "Do you want to delete {type} '{loc}'? This will move all products/boxes inside to the parent container."
    },
    box_detail_modal: {
      toasts: {
        success: {
          delete: "Successfully deleted box '{name}'",
          update: "Successfully updated box '{name}'"
        },
        error: {
          delete: "Error while deleting box '{name}'",
          update: "Error while updating box '{name}'"
        }
      },
      qr_code: "QR-Code for box '{box}'"
    }
  },
  de: {
    home: "Home",
    boxes: "Boxen",
    locations: "Orte",
    products: "Produkte",
    box: "Box",
    product: "Produkt",
    location: "Ort",
    save: "Speichern",
    not_found: "Die angeforderte Resource konnte nicht gefunden werden!",
    products_view:{
      products_in: "Produkte in {name}",
      starred_in: "Favorisierte Produkte in {name}"
    },
    add_modal: {
      select_product_placeholder: "Produkt auswählen",
      box_placeholder: "Box",
      location_placeholder: "Ort",
      amount_placeholder: "Menge",
      starred: "Favorisiert",
      product_name: "Name (Produkt)",
      location_name: "Name (Ort)",
      box_name: "Name (Box)",
      add_success_product: "Produkt '{name}' erfolgreich hinzugefügt",
      add_success_box: "Box '{name}' erfolgreich hinzugefügt",
      add_success_room: "Ort '{name}' erfolgreich hinzugefügt",
      add_btn_location: "Ort hinzufügen",
      add_btn_box: "Box hinzufügen",
      add_btn_product: "Produkt hinzufügen",
      add_new_product: "Neues Produkt hinzufügen",
      no_box: "Keine Box ausgewählt",
      no_room: "Kein Ort ausgewählt"
    },
    qr_data_modal: {

    },
    qr_reader_modal: {
      invalid_qr: "Bitte scannen Sie einen gültigen IH QR Code",
      title: "IH QR-Code scannen"
    },
    locations_view:{
      toasts: {
        success: {
          delete: "Ort '{name}' erfolgreich gelöscht"
        },
        error:{
          delete: "Ort '{name}' konnte nicht gelöscht werden"
        }
      },
    },
    boxes_overview: {
      boxes_in: "Boxen in {location}"
    },
    login_view: {
      username: "Username",
      password: "Passwort",
      register: "Registrieren",
      login: "Login",
      login_invalid: "Falscher Username / Falsches Passwort",
      toasts: {
        success: {
          register: "Registrierung erfolgreich"
        },
        error: {
          register: {
            username_taken: "Dieser Username ist bereits vergeben!",
            generic_error: "Ein Fehler ist aufgetreten, bitte versuche es später erneut!"
          }
        }
      }
    },
    settings_view: {
      settings: "Einstellungen",
      theme: "Theme",
      language: "Sprache"
    },
    room_detail_modal: {
      toasts:{
        success: {
          rename: "Umbenennen von Ort '{old}' zu '{new}' erfolgreich"
        },
        error: {
          rename: "Umbenennen von Ort '{old}' fehlgeschlagen"
        }
      },
      qr_code: "QR-Code für Ort '{loc}'"
    },
    product_detail_modal: {
      toasts: {
        success: {
          delete: "Produkt '{name}' erfolgreich gelöscht",
          update: "Produkt '{name}' erfoglreich aktualisiert",
          amountUpdate: "Menge von Produkt '{name}' erfoglreich aktualisiert"
        },
        error: {
          delete: "Fehler beim Löschen von Produkt '{name}'",
          update: "Fehler beim Aktualisieren von Produkt '{name}'",
          amountUpdate: "Fehler beim Aktualisieren der Menge von Produkt '{name}'"
        }
      },
      amount_below_zero: "Menge darf nicht unter null sein!"
    },
    room_card: {

    },
    box_card: {

    },
    products_card: {
      toasts: {
        success: {
          amountUpdate: "Menge von Produkt '{name}' erfoglreich aktualisiert"
        },
        error: {
          amountUpdate: "Fehler beim Aktualisieren der Menge von Produkt '{name}'"
        }
      },
    },
    home_view: {
      last_used: "⏰ Zuletzt verwendete Produkte",
      starred_products: "⭐ Favorisierte Produkte"
    },
    confirmation_modal: {
      box: "Box",
      location: "Ort",
      delete_product_expl: "Möchten Sie das Produkt (in allen Aufbewahrungsorten) löschen? Dann drücken Sie den roten Knopf.",
      delete_product_at_loc_expl: "Möchten Sie alle Produkte in Ort '{loc}' löschen? Dann drücken Sie den gelben Knopf.",
      delete_product_at_box_expl: "Möchten Sie alle Produkte in Box '{box}' löschen? Dann drücken Sie den gelben Knopf.",
      delete_product_at_def_expl: "Möchten Sie alle Produkte ohne Ort/Box löschen? Dann drücken Sie den gelben Knopf.",
      delete: "Löschen",
      delete_box: "Lösche Box",
      delete_location: "Lösche Ort",
      delete_product: "Alle",
      delete_product_at_loc: "Nur Dieses",
      delete_storage: "Möchten Sie {type} '{loc}' löschen? Diese Aktion wird alle Produkte/Boxen in den darüberliegenden Container verschieben."
    },
    box_detail_modal: {
      toasts: {
        success: {
          delete: "Box '{name}' erfolgreich gelöscht",
          update: "Box '{name}' erfolgreich aktualisiert"
        },
        error: {
          delete: "Fehler beim Löschen von Box '{name}'",
          update: "Fehler beim Aktualisieren von Box '{name}'"
        }
      },
      qr_code: "QR-Code für Box '{box}'"
    }
  },
  it: {
    home: "Home",
    boxes: "Box",
    locations: "Luoghi",
    products: "Prodotti",
    box: "Box",
    product: "Prodotto",
    location: "Posizione",
    save: "Salva",
    not_found: "La risorsa richiesta non è stata trovata!",
    products_view:{
      products_in: "Prodotti in {name}",
      starred_in: "Prodotto preferiti in {name}"
    },
    add_modal: {
      select_product_placeholder: "Seleziona prodotto",
      box_placeholder: "Scatola",
      location_placeholder: "Posizione",
      amount_placeholder: "Quantità",
      starred: "Preferiti",
      product_name: "Nome (Prodotto)",
      location_name: "Nome (Posizione)",
      box_name: "Nome (Scatola)",
      add_success_product: "Prodotto '{name}' aggiunto con successo",
      add_success_box: "Casella '{name}' aggiunta con successo",
      add_success_room: "Località '{name}' aggiunta con successo",
      add_btn_location: "Aggiungi luogo",
      add_btn_box: "Aggiungi scatola",
      add_btn_product: "Aggiungere prodotto",
      add_new_product: "Add new product",
      no_box: "No box selected",
      no_room: "No location selected"
    },
    qr_data_modal: {

    },
    qr_reader_modal: {
      invalid_qr: "Scansiona un codice QR IH valido",
      title: "Scansiona il codice QR IH"
    },
    locations_view:{
      toasts: {
        success: {
          delete: "Posizione '{name}' eliminata correttamente"
        },
        error:{
          delete: "Impossibile eliminare la località '{name}'"
        }
      },
    },
    boxes_overview: {
      boxes_in: "Scatole dentro {location}"
    },
    login_view: {
      username: "Username",
      password: "Password",
      register: "Registrare",
      login: "Login",
      login_invalid: "Username/password errata",
      toasts: {
        success: {
          register: "Iscrizione completata con successo"
        },
        error: {
          register: {
            username_taken: "Questo username è già in uso!",
            generic_error: "Si è verificato un errore, riprova più tardi!"
          }
        }
      }
    },
    settings_view: {
      settings: "Impostazioni",
      theme: "Tema",
      language: "Lingua"
    },
    room_detail_modal: {
      toasts:{
        success: {
          rename: "Ridenominazione della posizione '{old}' in '{new}' riuscita"
        },
        error: {
          rename: "Renaming location '{old}' failed"
        }
      },
      qr_code: "Codice QR per posizione '{loc}'"
    },
    product_detail_modal: {
      toasts: {
        success: {
          delete: "Prodotto '{name}' eliminato con successo",
          update: "Prodotto '{name}' aggiornato con successo",
          amountUpdate: "Quantità del prodotto '{name}' aggiornata con successo"
        },
        error: {
          delete: "Errore durante l'eliminazione del prodotto '{name'}",
          update: "Errore durante l'aggiornamento del prodotto '{name}'",
          amountUpdate: "Errore durante l'aggiornamento dell'importo del prodotto '{name}'"
        }
      },
      amount_below_zero: "L'importo non può essere inferiore a zero!"
    },
    room_card: {

    },
    box_card: {

    },
    products_card: {
      toasts: {
        success: {
          amountUpdate: "Quantità del prodotto '{name}' aggiornata con successo"
        },
        error: {
          amountUpdate: "Errore durante l'aggiornamento dell'importo del prodotto '{name}'"
        }
      },
    },
    home_view: {
      last_used: "⏰ Ultimi prodotti usati",
      starred_products: "⭐ Prodotti preferiti"
    },
    confirmation_modal: {
      box: "Box",
      location: "Posizione",
      delete_product_expl: "Vuoi eliminare il prodotto (in tutte le posizioni di archiviazione)? Quindi premere il pulsante rosso.",
      delete_product_at_loc_expl: "Vuoi eliminare tutti i prodotti nella posizione '{loc}'? Quindi premere il pulsante giallo.",
      delete_product_at_box_expl: "Vuoi eliminare tutti i prodotti nella casella '{box}'? Quindi premere il pulsante giallo.",
      delete_product_at_def_expl: "Vuoi eliminare tutti i prodotti senza posto/scatola? Quindi premere il pulsante giallo.",
      delete: "Spegnere",
      delete_box: "Eliminare la casella",
      delete_location: "Elimina posizione",
      delete_product: "Tutto",
      delete_product_at_loc: "Solo questo",
      delete_storage: "Vuoi eliminare {type} '{loc}'? Questa azione sposterà tutti i prodotti/scatole nel contenitore sopra."
    },
    box_detail_modal: {
      toasts: {
        success: {
          delete: "Casella '{name}' eliminata con successo",
          update: "Casella '{name}' aggiornata con successo"
        },
        error: {
          delete: "Errore durante l'eliminazione della casella '{name}'",
          update: "Errore durante l'aggiornamento della casella '{name}'"
        }
      },
      qr_code: "Codice QR per il box '{box}'"
    }
  }
}