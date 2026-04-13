# SceneChat

SceneChat is a text-driven scene generation pipeline that turns a natural language description into a structured room layout, previews the layout in Blender, and can optionally generate 3D assets for the objects in the scene.

## What it does

- Converts a scene description into structured JSON.
- Builds a Blender preview scene from the JSON layout.
- Supports an edit loop for modifying the scene description.
- Uses Meshy to generate 3D assets for scene objects.
- Saves preview `.blend` files and downloaded assets locally.

## Repository Layout

- `pipeline.py` - main interactive scene generation flow.
- `blenderapi/json2scene.py` - Blender helpers for building scenes from JSON.
- `blenderapi/json2mesh.py` - mesh-related utilities.
- `prompts/` - system prompts and cached model response samples.
- `outputs/` - generated Blender files and downloaded assets.
- `Reports/` - project report and LaTeX sources.

## Requirements

- Python 3.8+.
- Blender with Python `bpy` support.
- A working CUDA setup if you use the included DreamFusion-related environment.
- API access for:
  - `HYPERBOLIC_API_KEY`
  - `MESHY_API_KEY`

## Setup

Create an environment and install dependencies:

```bash
conda env create -f environment.yml
conda activate hlcv
```

If you prefer `pip`, install from `requirements.txt` inside a Python environment that already provides `bpy`:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root with your API keys:

```env
HYPERBOLIC_API_KEY=your_hyperbolic_key
MESHY_API_KEY=your_meshy_key
```

## Usage

Run the main pipeline from the project root:

```bash
python pipeline.py
```

The script will:

1. Ask for a scene description.
2. Load or produce a scene JSON description.
3. Create a Blender preview scene.
4. Ask whether you want to edit the scene.
5. Optionally generate 3D assets for the objects.

## Notes

- `pipeline.py` currently reads a cached response from `prompts/response.json` instead of calling the LLM path directly. This makes local testing deterministic.
- Generated files are written under `outputs/`.
- Blender import/export behavior depends on the installed Blender version and enabled importers.

