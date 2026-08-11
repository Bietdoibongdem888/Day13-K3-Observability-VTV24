# Alert và Runbook

Mỗi alert phải dựa trên triệu chứng người dùng hoặc SLO, không dựa trực tiếp vào tên implementation nội bộ.

## HighP95Latency

- Alert: P95 latency vượt 3000 ms liên tục 5 phút.
- Severity: critical.
- SLI/SLO liên quan: `latency_p95_ms <= 3000`, cửa sổ SLO 28 ngày.
- Symptoms: phản hồi chat chậm; tail latency tăng trong khi traffic có thể không đổi.
- Possible causes: retrieval chậm, model chậm hoặc saturation khi concurrency cao.
- Investigation: (1) xác định time window trên panel Latency và Traffic; (2) mở trace chậm, so sánh span retrieval và generation; (3) tìm log bằng correlation ID, kiểm tra `latency_ms`, feature và incident events.
- Immediate mitigation: giảm concurrency/rate, vô hiệu hóa incident practice nếu đang bật, hoặc tạm dùng retrieval fallback an toàn.
- Escalation: `observability-oncall`; báo owner retrieval/model nếu span tương ứng chiếm phần lớn latency.
- Long-term fix: timeout, circuit breaker, caching và alert theo burn rate.

## HighErrorRate

- Alert: error rate vượt 2% liên tục 5 phút.
- Severity: critical.
- SLI/SLO liên quan: `error_rate_pct <= 2`, cửa sổ SLO 28 ngày.
- Symptoms: request trả lỗi và `request_failed` tăng.
- Possible causes: dependency timeout, retrieval failure, lỗi validation hoặc regression ứng dụng.
- Investigation: (1) xem Traffic và Errors để loại trừ mẫu số nhỏ; (2) breakdown theo `error_type`; (3) mở trace lỗi rồi đối chiếu log cùng correlation ID.
- Immediate mitigation: rollback thay đổi gần nhất, cô lập dependency lỗi hoặc bật fallback đã được kiểm thử.
- Escalation: `observability-oncall`, sau đó owner dependency chứa span lỗi.
- Long-term fix: integration test cho error path, retry có giới hạn và error-budget burn alert.

## QualityDegradation

- Alert: mean quality proxy thấp hơn 0.75 liên tục 15 phút.
- Severity: warning.
- SLI/SLO liên quan: `quality_score_avg >= 0.75`, cửa sổ SLO 28 ngày.
- Symptoms: câu trả lời ngắn, thiếu context hoặc quality proxy giảm.
- Possible causes: prompt label sai, retrieval không khớp hoặc thay đổi response logic.
- Investigation: (1) đối chiếu Quality với Traffic/Error; (2) lọc trace theo prompt name/label/version; (3) kiểm tra retrieval span và log preview đã redact.
- Immediate mitigation: rollback label `production` về prompt baseline đã xác minh.
- Escalation: `ai-quality-owner`; phối hợp owner prompt/retrieval.
- Long-term fix: regression dataset, quality gate trước chuyển label và theo dõi quality theo prompt version.
