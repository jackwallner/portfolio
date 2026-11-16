// Counts App Store button taps per page and traffic source. No cookies, no
// personal data: one row of page, link campaign tag and source per tap.
(function () {
  var ENDPOINT = "https://kxlybsrsbibqkexffqmg.supabase.co/rest/v1/site_clicks";
  var KEY = "sb_publishable_By9FI1ctZMAZXCxHrQq8Xw_iwRIC0J6";

  function landingSource() {
    var src = "";
    try {
      src = new URLSearchParams(location.search).get("utm_source") || "";
      if (!src && document.referrer) {
        var host = new URL(document.referrer).hostname;
        if (host !== location.hostname) src = host;
      }
      if (src) sessionStorage.setItem("jw_src", src);
      else src = sessionStorage.getItem("jw_src") || "";
    } catch (e) {}
    return (src || "direct").replace(/^www\./, "").slice(0, 80);
  }

  var source = landingSource();

  document.addEventListener("click", function (ev) {
    var link = ev.target.closest && ev.target.closest('a[href*="apps.apple.com"]');
    if (!link) return;
    var ct = "";
    try { ct = new URL(link.href).searchParams.get("ct") || ""; } catch (e) {}
    try {
      fetch(ENDPOINT, {
        method: "POST",
        keepalive: true,
        headers: { apikey: KEY, "Content-Type": "application/json", Prefer: "return=minimal" },
        body: JSON.stringify({ page: location.pathname.slice(0, 200), ct: ct.slice(0, 80), source: source })
      });
    } catch (e) {}
  }, true);
})();
