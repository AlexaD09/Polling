// Decodificar JWT (una sola vez)
function parseJwt(token) {
  const base64Url = token.split('.')[1];
  const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
  const jsonPayload = decodeURIComponent(
    atob(base64)
      .split('')
      .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
      .join('')
  );
  return JSON.parse(jsonPayload);
}

// Enviar queja
async function enviarQueja() {
  const titulo = document.getElementById("tituloQueja").value.trim();
  const descripcion = document.getElementById("descripcionQueja").value.trim();

  const token = localStorage.getItem("access_token");

  if (!token) {
    alert("Debes iniciar sesión para enviar una queja.");
    window.location.href = "/index.html";
    return;
  }

  if (!titulo || !descripcion) {
    alert("Completa todos los campos");
    return;
  }

  // Decodificamos el token para extraer el id del usuario
  const decoded = parseJwt(token);
  const id_usuario = decoded.sub;
  const nombre = decoded.nombre;
  const email = decoded.email;

  const queja = {
    id_usuario: id_usuario,
    nombre:nombre,
    email:email,
    titulo: titulo,
    descripcion: descripcion,
    estado: "Pendiente"
  };

  console.log("Enviando queja:", queja);
  console.log("Token:", token);

  try {
    const response = await fetch("http://localhost:8001/quejas/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify(queja)
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Error al enviar la queja");
    }

    alert("Queja enviada con éxito");
    document.getElementById("quejaForm").reset();

  } catch (error) {
    console.error("Error al enviar la queja:", error.message);
    alert(error.message);
  }
}

async function cargarQuejas() {
  const token = localStorage.getItem("access_token");
  if (!token) return;

  const decoded = parseJwt(token);
  const id_usuario = decoded.sub;

  try {
    const response = await fetch(`http://localhost:8003/api/reporte/web/usuario/${id_usuario}`, {
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });

    if (!response.ok) throw new Error("No se pudieron cargar las quejas");

    const quejas = await response.json();
    const estadoQuejas = document.getElementById("estadoQuejas");
    estadoQuejas.innerHTML = "";

    if (!quejas || quejas.length === 0) {
      estadoQuejas.innerHTML = "<p class='text-muted'>No hay quejas registradas.</p>";
      return;
    }

    quejas.forEach(q => {
      const card = document.createElement("div");
      card.className = "card mb-3";
      card.innerHTML = `
        <div class="card-body">
          <h5 class="card-title">${q.titulo}</h5>
          <p class="card-text">${q.descripcion}</p>
          <span class="badge bg-warning text-dark">${q.estado}</span>
        </div>
      `;
      estadoQuejas.appendChild(card);
    });
  } catch (err) {
    console.error("❌ Error al cargar quejas:", err);
  }
}

// Evento para cerrar sesión
document.getElementById("btnLogout").addEventListener("click", function () {
  localStorage.removeItem("access_token");
  console.log("🔐 Token eliminado. Cerrando sesión...");
  window.location.href = "/index.html";  // Redirige al login o página de inicio
});

document.getElementById("quejaForm").addEventListener("submit", function (e) {
  e.preventDefault();
  enviarQueja().then(cargarQuejas);
});

window.onload = cargarQuejas;
