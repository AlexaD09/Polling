//usuarioservice
// Función para decodificar JWT (sin librerías externas)
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

document.getElementById("loginForm").addEventListener("submit", async function(e) {
  e.preventDefault();

  const correo = document.getElementById("correo").value;
  const contraseña = document.getElementById("contraseña").value;

  const res = await fetch("http://localhost:8000/usuarios/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ correo, contraseña })
  });

  const data = await res.json();

  if (res.ok) {
    const token = data.access_token;
     console.log("TOKEN RECIBIDO:", token);
    localStorage.setItem("access_token", token);
    

    const payload = parseJwt(token);

    //redirigir segun rol

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
    document.getElementById("mensaje").innerText = "Credenciales incorrectas";
  }
});
