// Escuchamos el evento "submit" del formulario con el id "registroForm"
document.getElementById("registroForm").addEventListener("submit", async function(e) {
  // Prevenimos que el formulario se envíe de forma tradicional (evita recargar la página)
  e.preventDefault();

  // Obtenemos y limpiamos los valores ingresados por el usuario
  const nombre = document.getElementById("nombre").value.trim();
  const correo = document.getElementById("correoRegistro").value.trim();
  const pssw = document.getElementById("contraseñaRegistro").value.trim();

  // Validamos que todos los campos tengan valor
  if (!nombre || !correo || !pssw) {
    // Si algún campo está vacío, mostramos un mensaje de error
    document.getElementById("mensaje").innerText = "Por favor completa todos los campos.";
    return; // Detenemos la ejecución si hay campos vacíos
  }

  // Hacemos una solicitud POST al backend para registrar al usuario
  const res = await fetch("http://localhost:8000/usuarios/registro", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ nombre, correo, pssw }),
});

// Convertimos la respuesta del servidor a un objeto JavaScript (JSON)
const data = await res.json();

// Comprobamos si la solicitud fue exitosa (código HTTP 200–299)
if (res.ok) {
  document.getElementById("mensaje").innerText = "Registro Exitoso";
  window.location.href = "/index.html";
} else {
  // Si hubo un error en el servidor o en los datos:
  console.error("Error backend:", data);
  document.getElementById("mensaje").innerText = data.detail || "Error en registro";
}

});

document.getElementById("registroForm").addEventListener("submit", async function(e) {
  e.preventDefault();

  const nombre = document.getElementById("nombre").value.trim();
  const correo = document.getElementById("correoRegistro").value.trim();
  const pssw = document.getElementById("contraseñaRegistro").value.trim();

  if (!nombre || !correo || !pssw) {
    document.getElementById("mensaje").innerText = "Por favor completa todos los campos.";
    return;
  }

  const res = await fetch("http://localhost:8000/usuarios/registro", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ nombre, correo, pssw }),
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
