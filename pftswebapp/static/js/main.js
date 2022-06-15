function clearTextArea() {
  document.getElementById("keyword").value = "";
  document.getElementById("keyword").focus();
}

function typeVelthuis(userKeyword) {
  /* pnry 09 Nov 2020 */
  return userKeyword
    .replace(/aa/g, "ā")
    .replace(/ii/g, "ī")
    .replace(/uu/g, "ū")
    .replace(/m\.\./g, "ṁ")
    .replace(/\.m/g, "ṃ")
    .replace(/\.n/g, "ṇ")
    .replace(/\.d/g, "ḍ")
    .replace(/\.l/g, "ḷ")
    .replace(/\.r/g, "ṛ")
    .replace(/\.s/g, "ṣ")
    .replace(/s\.\./g, "ś")
    .replace(/\.t/g, "ṭ")
    .replace(/,,n/g, "ñ")
    .replace(/n\.\./g, "ṅ")
    .replace(/AA/g, "Ā")
    .replace(/II/g, "Ī")
    .replace(/UU/g, "Ū")
    .replace(/M\.\./g, "Ṁ")
    .replace(/\.M/g, "Ṃ")
    .replace(/\.N/g, "Ṇ")
    .replace(/\.D/g, "Ḍ")
    .replace(/\.L/g, "Ḷ")
    .replace(/\.R/g, "Ṛ")
    .replace(/\.S/g, "Ṣ")
    .replace(/S\.\./g, "Ś")
    .replace(/\.T/g, "Ṭ")
    .replace(/,,N/g, "Ñ")
    .replace(/N\.\./g, "Ṅ");
}

function uTyping() {
  let t = document.getElementById("keyword");
  setTimeout(function() {
    t.value = typeVelthuis(t.value);
  }, 15);
}

function runOnStartUpLoaded() {
    document
    .getElementById("keyword")
    .addEventListener("input", uTyping, { passive: false });
    
    document
    .getElementById("clearText")
    .addEventListener("click", clearTextArea, { passive: false });
}

window.onload = runOnStartUpLoaded;
