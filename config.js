window.APP_CONFIG = {
  API_BASE:
    window.location.hostname === "localhost" ||
    window.location.hostname === "127.0.0.1"
      ? ""
      : "https://e-commerce-3-tgpq.onrender.com",
};
