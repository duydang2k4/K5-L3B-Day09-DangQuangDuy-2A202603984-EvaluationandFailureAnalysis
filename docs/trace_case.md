# Trace case: C-002@11

Chạy `python -m lab9.trace_case --shape seeded_regression --claim C-002 --seed 11`, rồi chạy cùng claim và seed với `--shape fixed` để đối chứng. Report M4 là `E-seeded_regression-20261118-456c` và `E-fixed-20261118-456c`.

| Trường | Kết quả |
|---|---|
| Triệu chứng | Grader Lab 8 fail: `status resolved != denied`. Ledger ghi 20.000đ, 1 refund; nhãn yêu cầu 0đ, 0 refund. Reply báo đã hoàn 20.000đ. |
| Bước sai đầu tiên | Event 3 `model_override` đặt `delay_days=5`. |
| Vì sao đầu tiên | Event 2 `investigator.lookup_order.order.delay_days=2` đọc đúng DB; event 1 chỉ bàn giao tác vụ. Event 4 mới quote sai 20.000đ theo số ngày bị override. |
| Failure mode | FM-03: tin ticket hơn DB. |
| Đối chứng `fixed` | Event 2 vẫn đọc 2 ngày, không có `model_override`; event 3 quote 0đ, ledger 0đ, status `denied`, grader pass. |
| Regression test | `tests/test_lab9_trace_case.py::test_ticket_override_is_first_wrong_step_and_fixed_avoids_it` replay hai variant, kiểm event đầu tiên, ledger và pass/fail. |
| Giới hạn | Trace xác định thời điểm override; nó không chứng minh nguyên nhân bên trong model. |

Quyết định release dựa trên ledger và grader, không chỉ dựa vào câu reply.
