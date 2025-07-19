//usuarioservice
// Función para decodificar JWT y extraer los datos del usuario o "payload"
function parseJwt(token) {
  let base64Url = token.split('.')[1];
  let base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
  let jsonPayload = decodeURIComponent(
    window.atob(base64)
      .split('')
      .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
      .join('')
  );

  return JSON.parse(jsonPayload);
}

// Agrega un evento "submit" al formulario con id "loginForm"
document.getElementById("loginForm").addEventListener("submit", async function(e) {
  // Evita que el formulario se envíe de forma tradicional (recargando la página)
  e.preventDefault();

   // Obtiene los valores ingresados por el usuario en los campos de correo y contraseña
  const correo = document.getElementById("correo").value;
  const contraseña = document.getElementById("contraseña").value;

   // Hace una solicitud POST al endpoint del backend para iniciar sesión
  const res = await fetch("http://localhost:8000/usuarios/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ correo, contraseña })
  });
  
  // Convierte la respuesta del servidor a un objeto JSON
  const data = await res.json();
 
  // Si la respuesta es exitosa (código 200-299)
  if (res.ok) {
     // Guarda el token recibido en localStorage para usarlo más adelante (ej: en rutas protegidas)
    const token = data.access_token;
     console.log("TOKEN RECIBIDO:", token);
    localStorage.setItem("access_token", token);
    
    // Decodifica el payload del token JWT para obtener información del usuario (como su rol)
    const payload = parseJwt(token);

    // Redirige al usuario a una página diferente según su rol

    if(payload.rol == "admin"){
      window.location.href = "/admin.html";
    }else if (payload.rol =="cliente"){
      window.location.href = "/cliente.html";
    }else if (payload.rol == "empleado"){
      window.location.href = "/empleado.html";
    }else{
      window.location.href = "/index.html";
    }
  } else {
    // Si el inicio de sesión falla, muestra un mensaje de error en la página
    document.getElementById("mensaje").innerText = "Credenciales incorrectas";
  }
});
