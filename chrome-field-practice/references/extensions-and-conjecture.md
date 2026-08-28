# Password managers and other extensions (CONJECTURE)

Everything below the baseline measurement is CONJECTURE, clearly labelled as such in the source field notes. Do not treat any of it as a measured cause of a failure unless you have independently confirmed it in this environment.

A standing rule in some engagements is "keep the password manager disabled" during automation. Whether it has ever actually caused a problem is unverified.

**Measured baseline** (password manager disabled, on a live Zoho Analytics page): zero password-manager DOM nodes, zero `chrome-extension://` iframes, 114 `input` elements on the page, none decorated.

**Mechanisms by which a password manager CAN interfere with browser automation** (general, not observed here): injecting icons and overlay iframes into or near input fields, which intercept clicks aimed at the field; mutating the DOM and invalidating cached selectors; stealing focus with an autofill prompt; adding a small amount of renderer work.

**Mechanisms by which it CANNOT cause the tab-visibility symptoms** (see SKILL.md, section 1): an extension cannot set `visibilityState` to hidden and cannot stop the compositor. Frame starvation is Chrome's tab lifecycle, not an extension's doing. The password manager is exonerated for that class of failure.

**Where suspicion is reasonable:** a page with over a hundred inputs is exactly the surface a password manager decorates. If trouble involves login flows or clicking into text fields specifically, interference is credible. Nothing in the current record confirms it either way.

**Independent reason to keep it disabled regardless of the above:** Claude must never enter credentials into a field. An extension that autofills them blurs that boundary. That is a governance argument, not a performance one, and it holds whether or not the extension has ever actually broken anything.

**Cheap A/B if the convenience is wanted back:** re-enable it, load the same page, re-run the baseline query above, and compare node counts. If the app surface is unchanged, the interference risk is low. Log the result either way (see "Keeping this skill current" in SKILL.md); this is exactly the kind of observation that should accumulate rather than get re-litigated from scratch each time.
