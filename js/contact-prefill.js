/* contact-prefill.js — pré-remplissage du formulaire de contact depuis une fiche œuvre.
   Le nom de l'œuvre est lu dans le titre affiché sur la page elle-même, puis transmis
   à l'accueil par sessionStorage (jamais par l'URL). La relecture se fait dans main.js,
   section CONTACT FORM. */
"use strict";

(function () {
  var titreEl = document.querySelector(".oeuvre-title");
  if (!titreEl) return;

  // textContent : le titre contient un <em>, on ne veut que le texte.
  var titre = titreEl.textContent.replace(/\s+/g, " ").trim();
  if (!titre) return;

  var surDemande = !!document.querySelector(".oeuvre-price.on-request");

  function memoriser(sujet, message) {
    try {
      sessionStorage.setItem("ah_contact_sujet", sujet);
      sessionStorage.setItem("ah_contact_message", message);
    } catch (e) { /* sessionStorage indisponible : le lien fonctionne quand même */ }
  }

  // Chaque bouton porte son propre sujet, distinct des deux autres.
  var btnAcq = document.querySelector("a.btn-acq");
  if (btnAcq) {
    btnAcq.addEventListener("click", function () {
      if (surDemande) {
        memoriser("Demande de prix",
          "Bonjour, je souhaiterais connaître le prix de l'œuvre « " + titre + " ».");
      } else {
        memoriser("Acquisition d'une œuvre",
          "Bonjour, je souhaite acquérir l'œuvre « " + titre + " ».");
      }
    });
  }

  var btnContact = document.querySelector("a.btn-contact");
  if (btnContact) {
    btnContact.addEventListener("click", function () {
      memoriser("Question sur une œuvre",
        "Bonjour, j'ai une question au sujet de l'œuvre « " + titre + " ».");
    });
  }
})();
