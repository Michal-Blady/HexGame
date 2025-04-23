export function initBoard(size, gameId, mode, role) {
  const legend       = document.getElementById("legend");
  const playAgainBtn = document.getElementById("play-again");
  const root         = document.getElementById("board");
  root.innerHTML     = "";

  let myColor = null;
  let gameOver = false;

  const wrap = document.createElement("div");
  wrap.id  = "board-wrapper";
  root.appendChild(wrap);

   const resultDiv = document.createElement("div");
  resultDiv.id = "result";
  resultDiv.style.display = "none";
  resultDiv.innerHTML = `
    <p id="result-text" style="font-size:24px; color:#fff; text-align:center;"></p>
  `;
  root.appendChild(resultDiv);

  const cells = [];
  const cellPx = Math.floor(
    Math.min(window.innerWidth, window.innerHeight - 50) / (size * 1.3)
  );
  document.documentElement.style.setProperty("--cell", `${cellPx}px`);

  for (let r = 0; r < size; r++) {
    const rowDiv = document.createElement("div");
    rowDiv.className = "row";
    rowDiv.style.marginLeft = `${r * cellPx * 0.5}px`;

    const row = [];
    for (let c = 0; c < size; c++) {
      const btn = document.createElement("button");
      btn.className  = "cell";
      btn.dataset.rc = `${r},${c}`;
      btn.addEventListener("click", () => {
        if (!btn.disabled && !gameOver) {
          sock.send(btn.dataset.rc);
        }
      });
      rowDiv.appendChild(btn);
      row.push(btn);
    }
    wrap.appendChild(rowDiv);
    cells.push(row);
  }

  const params = new URLSearchParams({ mode, role });
  const wsProto = location.protocol === "https:" ? "wss" : "ws";
  const sock = new WebSocket(
    `${wsProto}://${location.host}/ws/${gameId}?${params}`
  );

  sock.onopen = refresh;
  sock.onmessage = e => {
    if (e.data.startsWith("assign:")) {
      myColor = Number(e.data.split(":")[1]);
    }
    refresh();
  };

  async function refresh() {
    const res = await fetch(`/api/game/${gameId}`);
    const st  = await res.json();
    draw(st);
  }

  function draw(st) {
    if (mode === "local") {
      legend.textContent = "⬤ Tryb lokalny";
    } else {
      legend.textContent = (st.turn === myColor)
        ? "◼ Twoja tura"
        : "◻ Tura przeciwnika";
    }

    for (let r = 0; r < size; r++) {
      for (let c = 0; c < size; c++) {
        const btn = cells[r][c];
        const v   = st.grid[r][c];
        btn.className = "cell";

        if (v === 1) btn.classList.add("white");
        if (v === 2) btn.classList.add("black");

        if (r === 0   || r === size - 1) btn.classList.add("edge-black");
        if (c === 0   || c === size - 1) btn.classList.add("edge-white");

        btn.disabled = (
          v !== 0 ||
          st.winner !== null ||
          (mode !== "local" && st.turn !== myColor)
        );
      }
    }

    if (st.winner !== null && !gameOver) {
      gameOver = true;

      const who = st.winner === 2 ? "Black" : "White";
      alert(`🎉 Wygrał ${who}! 🎉`);

      playAgainBtn.style.display = "inline-block";
    }
  }

  playAgainBtn.addEventListener("click", async () => {
    await fetch(`/api/game/${gameId}`, { method: "DELETE" });
    window.location = `/?mode=${mode}`;
  });

  refresh();
}
