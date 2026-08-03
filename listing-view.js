document.addEventListener("DOMContentLoaded", () => {
  const toolbar = document.querySelector("[data-listing-view-toggle]");
  const listing = document.querySelector(".quarto-listing-container-default");

  if (!toolbar || !listing) {
    return;
  }

  listing.classList.add("listing-view-enabled");

  const buttons = Array.from(toolbar.querySelectorAll("[data-listing-view]"));
  const storageKey = "sbilmis-listing-view";

  const setView = (view, remember = true) => {
    const selected = view === "cards" ? "cards" : "list";
    listing.dataset.view = selected;

    buttons.forEach((button) => {
      button.setAttribute(
        "aria-pressed",
        String(button.dataset.listingView === selected),
      );
    });

    if (remember) {
      try {
        window.localStorage.setItem(storageKey, selected);
      } catch {
        // The view still works when browser storage is unavailable.
      }
    }
  };

  buttons.forEach((button) => {
    button.addEventListener("click", () => setView(button.dataset.listingView));
  });

  let initialView = "list";
  try {
    initialView = window.localStorage.getItem(storageKey) || initialView;
  } catch {
    // Keep the quiet list view as the default.
  }

  setView(initialView, false);
});
