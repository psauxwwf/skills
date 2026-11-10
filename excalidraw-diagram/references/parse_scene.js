// Shared by the browser renderer and dependency-free Node regression tests.
function parseExcalidrawSource(source, decompressFromBase64) {
  if (typeof source !== "string") return validate(source);

  const text = source.replace(/^\uFEFF/, "").trim();
  if (text.startsWith("{")) return validate(JSON.parse(text));

  // Ignore JSON examples in Text Elements; only read the Drawing section.
  const drawing = /^#{1,6}[ \t]+Drawing[ \t]*\r?$/m.exec(text);
  if (!drawing) throw new Error("No Excalidraw Drawing section found in Markdown");

  const section = text.slice(drawing.index + drawing[0].length);
  const block = /^[ \t]*```(json|compressed-json)[ \t]*\r?\n([\s\S]*?)\r?\n[ \t]*```[ \t]*(?:\r?$)/m.exec(section);
  if (!block) throw new Error("No json/compressed-json block found in Drawing section");

  let json = block[2];
  if (block[1] === "compressed-json") {
    // Obsidian wraps base64 payloads across multiple lines.
    json = decompressFromBase64(json.replace(/\s/g, ""));
    if (!json) throw new Error("Could not decompress Excalidraw Drawing data");
  }
  return validate(JSON.parse(json));

  function validate(data) {
    if (!data || data.type !== "excalidraw" || !Array.isArray(data.elements)) {
      throw new Error("Invalid Excalidraw scene: expected type excalidraw and an elements array");
    }
    return data;
  }
}

if (typeof module !== "undefined") module.exports = { parseExcalidrawSource };
