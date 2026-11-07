# NovaCHAT

**Connect Everything.**

全新的社交通訊 Web App。單檔 HTML PWA + Python 後端（與既有可部署架構一致）。

- 版本：Phase 1 — 聊天頁（Chat）UI
- 視覺基準：Figma 440×956（iPhone 18 Pro Max）
- 技術：原生 HTML / CSS / JS（單檔 `index.html`）、Service Worker（離線 / 可安裝）、Python 內建 HTTP server

## 執行

```bash
py server.py
```

或直接用瀏覽器開 `index.html`（部分 PWA 功能需經伺服器）。

## 目前狀態（Phase 1）

聊天頁 UI 完成：
- 頂部品牌 + 標題 + 搜尋
- 搜尋好友 / 群組 / 聊天紀錄（即時過濾、無結果狀態）
- 分類：全部 / 未讀 / 群組
- 聊天列表：頭像、名稱、最新訊息預覽、時間、未讀數、已讀／送達狀態、靜音標示、群組標記
- 底部 Tab Bar 保留 5 格（聊天為目前頁；其餘待 Figma 確認，未擅自決定）
- 深 / 淺色主題、手機與桌面響應式

## 架構原則

- UI 從資料層 `Store` 渲染；目前用本地**範例資料（SEED）**，**非偽造後端**。
- 真後端（帳號 / 好友 / 群組 / 即時 / 推播）為下一階段；接上時只需把 `Store.fetchChats()` 改為 `fetch('/api/chats')`，UI 不動。
- `server.py` 的 `/api/chats` 目前明確回 `501 not_implemented`，不假裝已完成。

## 下一階段（未開工）

- 對話頁（文字 / 圖片 / 檔案 / 語音 / 表情 / 回覆 / 撤回 / 傳送狀態 / 群組）
- 真實帳號、好友、群組、即時通訊、推播
- 其餘 4 個導覽頁（待 Figma 設計確認）
