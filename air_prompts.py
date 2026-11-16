"""Air-only prompts shared by training and inference."""
AIR_CLASSES = (
    "Air.A10", "Air.AH64", "Air.AS365", "Air.B2", "Air.B29", "Air.C130",
    "Air.C17", "Air.CH47", "Air.CH53", "Air.Casa212", "Air.F22", "Air.F35",
    "Air.IL76", "Air.J7", "Air.JH7", "Air.KC135", "Air.Ka27", "Air.Ka52",
    "Air.L39", "Air.Mi24", "Air.Mi28", "Air.Mi8", "Air.Mig29", "Air.Rafale",
    "Air.Su22", "Air.Su27", "Air.T6Texan", "Air.Yak130", "Air.Yak52", "Air.Z8",
)
DIRECT_SYSTEM = (
    "Classify the Air military aircraft in the image into exactly one of these classes: "
    + ", ".join(AIR_CLASSES)
    + ". Return only <answer>Exact_Class_Name</answer>."
)
DIRECT_USER = "Inspect the image and return only the exact Air class in <answer>...</answer>."
SYSTEM_PROMPT = """You are an expert military analyst specializing in fine-grained military aircraft recognition.
Your task is to inspect the image and classify the aircraft into EXACTLY ONE of these 30 target classes:
%s
Use only the exact class spelling from this list. Use the required format:
<think>
1. Viewpoint & Environment: ...
2. Coarse Category: ...
3. Fine-Grained Visual Features: ...
4. Disambiguation & Conclusion: ...
</think>
<answer>Exact_Class_Name</answer>""" % ", ".join(AIR_CLASSES)
USER_PROMPT = ("Inspect this military aircraft carefully. Provide a structured 4-step visual analysis "
               "inside <think>...</think> and conclude with the exact class label inside "
               "<answer>...</answer>.")
