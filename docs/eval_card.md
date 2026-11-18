# Eval card — LogiX-VN refund agent

## V1 / Core

- Baseline run `E-swarm-20261118-456c`, fixed run `E-fixed-20261118-456c`, regression run `E-seeded_regression-20261118-456c`; eval-set SHA `456ccef33917`.
- MockLLM, 14 item × 5 seed (11, 22, 33, 44, 55); nhãn tách trong `src/data/eval/labels_v1.json`. Spec `src/config/metric_spec.yaml` v1.0. Các report nằm trong `src/reports/`.
- Baseline: `pass_rate=0.9857`, `refund_amount_correct=0.9857`, `approval_bypass=0`, `secret_leak=0`, `reply_ledger_match=1.0`. Fixed: `pass_rate=1.0`. Seeded regression: `pass_rate=0.7143`.
- Paired bootstrap theo item: seeded regression − baseline, `pass_rate` Δ −0.271, CI 95% [−0.500, −0.057]. Gate chặn regression ở `pass_rate`; `fixed` qua gate.
- Judge replay: tone κ 0.757, P 0.857, R 0.8 đạt floors; helpful κ 0.375, P 1.0, R 0.3 bị loại khỏi gate. Xem `docs/judge_audit.md`.
- Trace case `C-002@11`: event 3 `model_override` đổi `delay_days` từ 2 thành 5; xem `docs/trace_case.md` và test replay.

## V2 / Advanced–Expert

- Baseline run `E-swarm-20261118-fb4f`, eval-set SHA `fb4f590a6587`; 28 item × 5 seed. Spec `src/config/metric_spec_v2.yaml` v2.0.
- Baseline `pass_rate=0.9786`, `pass_hat_5=0.8929`, `reply_ledger_match=1.0`. Sàn `pass_hat_5=0.80` thấp hơn cả hai lượt A/A (seed spec và 66,77,88,99,110 đều 0.8929; Δ=0 trên MockLLM).
- Mutation scorecard: 3/3 regression bị chặn, 0 báo nhầm trên `fixed` và `honest_refactor`. `slice_regression` bị chặn bởi `money_movement/pass_rate`; `flaky_regression` bị chặn bởi `pass_hat_5` (cùng các metric khác). Hai slice `money_movement` và `adversarial` là blocking.
- Bốn trap công khai đều bị chặn: evaluator errors/NaN, dropped rows, cherry-picked seeds, loosened spec. Trên LLM thật, A/A có thể có dải nhiễu >0; phải đo lại dải này và đặt sàn ngoài vùng dao động trước khi dùng gate.

## Phạm vi và giới hạn

Eval chỉ dùng MockLLM, fixture công khai và judge replay; chưa có dữ liệu người dùng hoặc judge held-out. V1 chỉ có 14 item nên CI rộng. Với 5 seed, một lỗi xảy ra khoảng 1/3 seed có thể không được phát hiện ổn định. Hidden variants/traps của giảng viên chưa được kiểm ở repo này. Khi thêm item hoặc thay nhãn, tăng eval-set version và chạy lại baseline; khi đổi metric hoặc ngưỡng, tăng metric-spec version và ghi lý do. Chủ bản fork xử lý gate đỏ trước khi merge; không miễn trừ tự động.
