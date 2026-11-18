# Judge audit (CSV replay công khai, n=100 mỗi tiêu chí)

Lệnh: `python -m lab9.judge --csv data/eval/judge_tone_public.csv --audit 8` và tương tự với `judge_helpful_public.csv`. FAIL là lớp dương.

| Tiêu chí | TP / FP / FN / TN | κ | Precision | Recall | Kết luận |
|---|---|---:|---:|---:|---|
| tone_ok | 24 / 4 / 6 / 66 | 0.757 | 0.857 | 0.800 | Đạt floors κ≥0.6, P≥0.8, R≥0.7; có thể dùng để theo dõi tone. |
| helpful | 9 / 0 / 21 / 70 | 0.375 | 1.000 | 0.300 | Không đạt κ và recall; loại khỏi gate. |

## Audit bất đồng

| Case | Human / judge | Ai đúng? | Sửa rubric / nhãn |
|---|---|---|---|
| H-008 | FAIL / PASS | Human | Nêu rõ xưng “em”, “nha” quá suồng sã trong ngữ cảnh khiếu nại. |
| H-017 | FAIL / PASS | Human | Thêm hướng dẫn xưng hô trung tính “anh/chị”; không coi “bạn ơi” mặc định phù hợp. |
| H-029 | FAIL / PASS | Human | Cấm câu ra lệnh như “không cần nhắn thêm” dù mở đầu lịch sự. |
| H-042 | PASS / FAIL | Human | Không bắt buộc lời xin lỗi nếu câu trả lời ngắn, lịch sự và đủ nội dung. |
| H-063 | FAIL / PASS | Human | Hứa hoàn thêm ngoài kết quả hệ thống là lỗi; kiểm lời hứa với ledger bằng code. |
| H-070 | FAIL / PASS | Human | Emoji cười trong khiếu nại là tone không phù hợp. |
| H-081 | PASS / FAIL | Judge | Ghi chú CSV xác nhận nhãn người đọc nhầm ticket; sửa nhãn sau adjudication, không ép judge theo nhãn sai. |

`tone_ok` có observed failure rate 0.28, Rogan–Gladen ước tính 0.30 trên chính replay này. `helpful` có 21/30 lỗi thật bị bỏ sót; precision 1.0 không bù được recall 0.3, nên không dùng làm release gate. Các con số là trên CSV công khai, chưa có held-out hay nhãn người mới.
