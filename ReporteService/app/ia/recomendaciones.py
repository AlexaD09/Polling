from groq import Groq
from dotenv import load_dotenv
import os
from typing import List
from ReporteService.app.models.dto_reporte import QuejaCombinadaDTO

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
qclient = Groq(api_key=GROQ_API_KEY)

def resumen_a_texto(quejas: List[QuejaCombinadaDTO]) -> str:
    resumen = {}
    for q in quejas:
        estado = getattr(q, "estado", "Desconocido").strip().capitalize()
        resumen[estado] = resumen.get(estado, 0) + 1
    return ", ".join(f"{k}: {v}" for k, v in resumen.items())

async def generar_recomendaciones(quejas: List[QuejaCombinadaDTO]) -> str:
    if not quejas:
        return "No hay quejas para analizar."

    texto_resumen = resumen_a_texto(quejas)
    prompt = (
        f"Estos son los estados y cantidades de quejas: {texto_resumen}. "
        "Con base en esta información, dame una recomendación detallada para mejorar la atención."
    )

    try:
        response = qclient.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Error en la llamada a Groq:", str(e))
        return "Error al generar la recomendación."