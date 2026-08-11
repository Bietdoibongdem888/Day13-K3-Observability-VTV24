# Demo flow — Day 13 K3

## Chuẩn bị

1. Xác nhận `.env` local được ignore và có Langfuse credentials, không hiển thị key.
2. Khởi động Uvicorn không dùng reload, poll `/health` tới HTTP 200.
3. Giữ server chạy trong suốt smoke test, load test, dashboard và incident; chỉ dừng đúng PID đã tạo khi kết thúc.

## Kịch bản trình bày

1. Mở `/health`: HTTP 200, `tracing_enabled=true`.
2. Gửi `/chat` bằng payload trong sample data và lấy correlation ID từ response.
3. Tìm JSON log cùng correlation ID, chỉ ra enrichment và PII redaction.
4. Mở Langfuse trace tương ứng, giải thích root `run` → `retrieval` và `fake-llm`.
5. Chỉ ra trace metadata: correlation ID, session, feature, model, environment và prompt version.
6. Trình bày V1 trace `914192aa065813285f7fca37ded1c197`.
7. Promote production sang V2 và trình bày trace `07ffc195d58f71d1cc4054a668923545`.
8. Roll back production về V1 và trình bày trace `aa480f2d7814da903894ba4daf53cceb`.
9. Mở `/dashboard`, xác nhận sáu panel, cửa sổ 60 phút, refresh 30 giây, units và thresholds.
10. Giải thích SLO 28 ngày, ba alert rules và runbooks.
11. Chạy official `rag_slow`: baseline p95 151 ms → incident p95 2653 ms.
12. Từ metric window mở trace `16229089282a1f8b8fd1232620e96cb7`.
13. Chỉ ra retrieval span `f6fd112443631073` mất 2.503 s, trong khi fake LLM mất 0.151 s.
14. Dùng correlation ID `req-7506187a` tìm log `response_sent`, `feature=refund`, `latency_ms=2653`.
15. Kết luận root cause, immediate mitigation, permanent fix và preventive measure.
16. Kết thúc bằng 30 tests pass, log validator 100/100, dashboard validator 6/6, security audit và Git contribution thật.

Không trình bày API evidence như ảnh UI. Nếu rubric yêu cầu Langfuse screenshot, đăng nhập UI và chụp đúng các trace IDs đã ghi trong report.
