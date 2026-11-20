# Build rounds

A landing page is never right on the first build. The owner reads the screenshots, says what is
wrong, and the next round fixes it. These rules keep each round cheap, reversible and checkable.

## 1. Modes

| Mode | Start from | Skip |
|---|---|---|
| FULL BUILD | a brief and a reference URL | nothing |
| BUILD FROM COPY | finished copy from the owner or a copywriter | landing-copy writing steps; still run `copy_lint.py` and the copy gate |
| TEARDOWN | a live page that underperforms | the build; run recon on the page itself, then cro-audit and first-screen-check, and return a ranked fix list |
| REVISION ROUND | the owner's feedback on round N | recon; re-read the reference first screen anyway |

## 2. Before round 1

1. `templates/brief-checklist.md` filled. Every blank line is a question for the owner.
2. Recon of the reference (reference-recon) and `reference-map.md` filled.
3. `architecture.md` written: page job, the design read line, one job per section, friction budget,
   what was cut. Nothing gets built that is not in it.
4. `facts.md` started: every number the page will show, with a source.

## 3. Every round

1. **Back up first.** Copy the current page to `page-vN.html` (and the CSS to `site-vN.css`) before
   touching anything. Never overwrite a page that has been shown or shipped; keep a `.prev/` folder.
2. **Re-read the reference first screen.** Open `ref-first-screen.png` again. Drift from the
   reference happens one small round at a time.
3. **Map the feedback.** Write each point of the owner's message as a line, with the file and block it
   touches. Points that conflict with the architecture go back to the owner as a question.
4. **Edit through a build script, not by hand,** when a round touches more than two blocks. A script
   that does `rep(old, new)` and fails loudly when `old` is missing or appears twice is the cheapest
   insurance against a silent no-op edit. Keep the script with the round.
5. **Append CSS, do not rewrite it.** New rules go at the end under a marker
   `/* ===== vN ===== */`, so the diff per round is readable and a round can be rolled back.
6. **Run the gates.** `copy_lint.py`, `design_lint.py`, `gates.py`, `shot.py`, `first_screen.py`.
   All green or the round is not done.
7. **Read every screenshot slice** at 390 and 1440. The scripts catch wiring; only eyes catch a block
   that looks wrong.
8. **Report point by point.** Each line of the owner's feedback, then what changed and where. Points
   not done get a reason.

## 4. Traps that cost a round each

| Trap | What happens | Rule |
|---|---|---|
| Class collision | a new `.tree` or `.ab` block picks up rules from an older stylesheet and renders wrong | prefix new classes per block; list them in `gates.json` `classes` |
| Heredoc with backslashes | a shell heredoc turns `\b` or `\n` inside JS or regex into something else | build strings with `chr(92)` in Python, or write files with an editor tool |
| Long heredoc | the shell cuts a very long heredoc and the file ends mid-tag | split into several files or several writes |
| Lazy image above the fold | the hero renders blank in full-page screenshots | no `loading="lazy"` in the first two sections |
| Autoplay video blank | a video with no poster shows an empty box until it plays | `muted playsinline` plus a `poster` |
| Edited the wrong copy | the fix lands in `page-v3.html`, the preview serves `index.html` | the build script writes one path; gates run on that path |
| Live deploy by accident | a preview command pointed at production | preview deploys only; going live is the owner's call |

## 5. Done

The round is done when every gate is green, the screenshots were read, the report maps every
feedback point, and the backup of the previous round exists.
