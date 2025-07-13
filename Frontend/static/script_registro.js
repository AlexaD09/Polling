document.getElementById("registroForm").addEventListener("submit", async function(e) {
  e.preventDefault();

  const nombre = document.getElementById("nombre").value.trim();
  const correo = document.getElementById("correoRegistro").value.trim();
  const contraseña = document.getElementById("contraseñaRegistro").value.trim();

  if (!nombre || !correo || !contraseña) {
    document.getElementById("mensaje").innerText = "Por favor completa todos los campos.";
    return;
  }

  const res = await fetch("http://localhost:8000/usuarios/registro", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ nombre, correo, contraseña }),
});

const data = await res.json();

if (res.ok) {
  document.getElementById("mensaje").innerText = "Registro Exitoso";
  window.location.href = "/index.html";
} else {
  console.error("Error backend:", data);
  document.getElementById("mensaje").innerText = data.detail || "Error en registro";
}

});
