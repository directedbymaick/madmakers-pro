(function () {
  var CONSENT_KEY = 'cp-cookie-consent';
  var CONSENT_MAX_AGE = 180 * 24 * 60 * 60 * 1000;
  var GA4_ID = 'G-KVV7C90TRY';
  var CLARITY_ID = 'wrwxcnutw8';
  var banner = document.getElementById('cookie-banner');
  var trackingLoaded = false;

  function readConsent() {
    try {
      var stored = JSON.parse(localStorage.getItem(CONSENT_KEY));
      if (!stored || !stored.value || !stored.savedAt) return null;
      if (Date.now() - stored.savedAt > CONSENT_MAX_AGE) {
        localStorage.removeItem(CONSENT_KEY);
        return null;
      }
      return stored.value;
    } catch (error) {
      return null;
    }
  }

  function saveConsent(value) {
    try {
      localStorage.setItem(CONSENT_KEY, JSON.stringify({ value: value, savedAt: Date.now() }));
    } catch (error) {}
  }

  function setGoogleConsent(value) {
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
    window.gtag('consent', 'update', {
      analytics_storage: value === 'accepted' ? 'granted' : 'denied',
      ad_storage: 'denied',
      ad_user_data: 'denied',
      ad_personalization: 'denied'
    });
  }

  function setClarityConsent(value) {
    window.clarity = window.clarity || function () {
      (window.clarity.q = window.clarity.q || []).push(arguments);
    };
    window.clarity('consentv2', {
      ad_Storage: 'denied',
      analytics_Storage: value === 'accepted' ? 'granted' : 'denied'
    });
  }

  function loadTracking() {
    if (trackingLoaded) return;
    trackingLoaded = true;
    setGoogleConsent('accepted');
    var ga = document.createElement('script');
    ga.async = true;
    ga.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA4_ID;
    document.head.appendChild(ga);
    window.gtag('js', new Date());
    window.gtag('config', GA4_ID, { cookie_flags: 'SameSite=Strict;Secure' });

    setClarityConsent('accepted');
    var clarityScript = document.createElement('script');
    clarityScript.async = true;
    clarityScript.src = 'https://www.clarity.ms/tag/' + CLARITY_ID;
    document.head.appendChild(clarityScript);
  }

  function showBanner() {
    if (banner) banner.style.display = 'flex';
  }

  function hideBanner() {
    if (banner) banner.style.display = 'none';
  }

  function applyConsent(value) {
    saveConsent(value);
    hideBanner();
    if (value === 'accepted') loadTracking();
    else {
      setGoogleConsent('refused');
      setClarityConsent('refused');
      if (trackingLoaded) window.location.reload();
    }
  }

  var consent = readConsent();
  var settingsRequested = new URLSearchParams(window.location.search).get('cookies') === 'manage';
  if (consent === 'accepted') loadTracking();
  else if (consent === 'refused') {
    setGoogleConsent('refused');
    setClarityConsent('refused');
  } else setTimeout(showBanner, 600);
  if (settingsRequested) setTimeout(showBanner, 100);

  var accept = document.getElementById('cookie-accept');
  var refuse = document.getElementById('cookie-refuse');
  var settings = document.getElementById('cookie-settings');
  if (accept) accept.addEventListener('click', function () { applyConsent('accepted'); });
  if (refuse) refuse.addEventListener('click', function () { applyConsent('refused'); });
  if (settings) settings.addEventListener('click', function () {
    showBanner();
  });
})();
