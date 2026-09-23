import os
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "Astrea",
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 8000)),
)

MESHY_URL = "https://api.meshy.ai/openapi/v2/text-to-3d"


def entetes():
    cle = os.environ.get("MESHY_API_KEY", "")
    return {"Authorization": f"Bearer {cle}"}


@mcp.tool()
def test_astrea() -> str:
    """Test gratuit : vérifie que le serveur Astrea répond."""
    return "Astrea est en ligne."


@mcp.tool()
def creer_modele_3d(description: str) -> str:
    """Lance la création d'un modèle 3D (sans texture) à partir d'une description en anglais."""
    reponse = httpx.post(
        MESHY_URL,
        headers=entetes(),
        json={"mode": "preview", "prompt": description, "should_remesh": True},
        timeout=30,
    )
    reponse.raise_for_status()
    return reponse.json()["result"]


@mcp.tool()
def voir_modele_3d(id_tache: str) -> dict:
    """Donne l'état d'un modèle 3D et ses liens de téléchargement quand il est prêt."""
    reponse = httpx.get(f"{MESHY_URL}/{id_tache}", headers=entetes(), timeout=30)
    reponse.raise_for_status()
    donnees = reponse.json()
    return {
        "statut": donnees.get("status"),
        "progression": donnees.get("progress"),
        "liens": donnees.get("model_urls"),
    }


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
