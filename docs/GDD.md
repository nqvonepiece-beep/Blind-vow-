# Blind Vow - Tài liệu thiết kế (GDD)

Bản đồng bộ từ tài liệu bàn giao. Các mục ghi "đề xuất" là chưa được Vinny duyệt, chưa phải quyết định.

## 1. Tổng quan

- Tên: **Blind Vow**.
- RPG hành động thế giới mở trên Roblox, fantasy trung cổ châu Âu pha yếu tố isekai.
- Combat **nhanh và căng** kiểu Deepwoken: parry, block, né, stamina, posture.
- **Chết vĩnh viễn:** nhân vật chết là mất hẳn. Server quyết định cái chết. Lỗi lưu dữ liệu tạm thời không bao giờ được xóa nhầm nhân vật.
- Hỗ trợ chơi một mình và chơi nhóm.
- Tham khảo (chỉ lấy cảm hứng, không sao chép nội dung): Deepwoken, Rune Slayer, Pilgrammed, Rogue Lineage, Voxlblade, anime isekai.

## 2. Cốt truyện

- Player vốn là kiếm sĩ mạnh của thế giới này, yêu Mikami và hy sinh.
- Mikami muốn hồi sinh Player nên ký khế ước với ác quỷ. Linh hồn Player đã đầu thai ở thế giới khác, bị kéo về thế giới cũ cùng thân xác mới, khoảng 18 tuổi.
- Mikami tiến vào thế giới mới của Player, giết chị gái của Player rồi giả dạng làm chị gái. Thật ra chị gái thật không chết mà bị giam cầm ở một vùng đất thuộc một lục địa nào đó (chi tiết để sau, ai giam cũng để sau).
- Player chỉ biết sự thật gần cuối truyện, sau khi hoàn thành một nhiệm vụ và gặp được chị.
- Cốt truyện xoay quanh Player và hành trình khám phá thế giới.

## 3. Nhân vật và phản diện

| Nhân vật | Vai trò | Phong cách chiến đấu |
| --- | --- | --- |
| Boss làng tân thủ (chưa có tên) | Quý tộc có tiếng, cha của NPC bạn đồng hành; âm mưu tiến hóa con người và ma thuật bằng thí nghiệm trên người. Tóc xanh, da trắng, mắt xanh, cao ráo, trang phục quý tộc | Phép gió, cận chiến, điều khiển các vật thí nghiệm tấn công |
| Mikami | Người yêu của Player ở kiếp trước, người đưa Player đến thế giới này; giả dạng chị gái của Player; bị ác quỷ điều khiển; đồng minh lúc đầu, boss cuối về sau vì mục tiêu cá nhân | Kiếm thuật, phép thuật, cận chiến, ma pháp; nổi trội ở ma pháp không gian |
| Player | Kiếm sĩ mạnh, từng hy sinh vì Mikami, nay tái sinh khoảng 18 tuổi | Tùy chủng tộc và class do người chơi chọn |

Chưa có: tên boss làng tân thủ, tên NPC bạn đồng hành, ngoại hình Mikami.

## 4. Chủng tộc (9)

Human, Elf, Dwarf, Orc, Goblin, Beastkin, Dragonkin, Demonkin, Tidekin.

Điểm mạnh và yếu sơ bộ (đề xuất, chưa cân bằng):

- Human: linh hoạt, học nhanh; không nổi bật.
- Elf: nhanh, mạnh phép, giỏi cung; máu thấp, yếu khi bị áp sát.
- Dwarf: nhiều máu và giáp, hợp rèn đúc; chậm, phép kém.
- Orc: sức mạnh và máu cao, đòn nặng; kỹ thuật kém, chậm.
- Goblin: nhỏ, nhanh, khéo tay, giỏi bẫy và chế tạo; máu thấp, sát thương đơn lẻ yếu.
- Beastkin: tốc độ, giác quan nhạy, cận chiến mạnh; phòng thủ phép yếu.
- Dragonkin: sức mạnh thô, kháng lửa; tốn stamina, thân to nên dễ bị đánh trúng.
- Demonkin: phép tối, hồi phục khi gây sát thương; yếu trước phép thánh, bị NPC nghi kỵ.
- Tidekin: mạnh gần nước, bơi và nín thở giỏi; yếu nơi khô cạn.

## 5. Class (10 Basic Class)

Người chơi có thể thử vũ khí trước khi chọn class, hoặc bắt đầu trực tiếp bằng một Basic Class. Không ép mọi người phải trải qua cùng một quy trình.

| Class | Vai trò | Cơ chế | Hướng phát triển |
| --- | --- | --- | --- |
| Warrior | Cận chiến tổng quát, thích ứng nhiều vũ khí | Weapon Mastery, Combat Technique, Adaptation | Swordsman, Weapon Vanguard, Breaker |
| Knight | Phòng thủ, bảo vệ, kiểm soát khoảng cách, phản đòn | Guard, Counter, Oath, Protection | Guardian, Oath Knight, Curse Knight, Cavalier |
| Rogue | Cơ động, né tránh, ám kích, bẫy, khai thác sơ hở | Evasion, Stealth, Precision, Trickery | Assassin, Thief, Trickster, Rogue Duelist |
| Mage | Ma thuật nguyên tố, ma pháp cổ, kết giới, biến đổi mana | Mana, Elemental Magic, Arcane, Spellcraft | Elementalist, Arcanist, Enchanter, Curse Mage, Battle Mage |
| Archer | Tấn công tầm xa, ngắm bắn, kiểm soát khoảng cách | Aim, Mark, Precision, Projectile | Sniper, Ranger, Trapper, Arcane Archer |
| Cleric | Hồi phục, thanh tẩy, kết giới, hỗ trợ hoặc chiến đấu trực diện | Healing, Purification, Divine Power, Wards | Priest, Exorcist, Oracle, Inquisitor, Battle Cleric |
| Monk | Võ thuật tay không, nhịp combo, tư thế, nội lực, phản đòn | Chi, Combo, Stance, Body Control | Martial Artist, Chi Adept, Shadow Monk, Iron Body Monk |
| Barbarian | Sát thương cao, sức bền, đánh đổi rủi ro | Rage, Resolve, Brutal Force, Risk | Berserker, Warlord, Beast Savage, Blood Berserker |
| Lancer | Đâm, lao kích, giữ khoảng cách, ngăn đối thủ áp sát | Reach, Thrust, Impale, Mobility | Spear Adept, Phalanx, Wind Lancer, Dragon Lancer |
| Summoner | Triệu hồi sinh vật, linh thể, thực thể khế ước hoặc tạo vật | Summoning, Binding, Companions, Command | Beast Tamer, Spirit Caller, Golemancer, Necromancer, Pact Summoner |

Class khó làm nhất, để làm sau cùng: Summoner (cần AI riêng cho thú triệu hồi) và Cleric (hồi phục khó cân bằng trong PvP).

## 6. Hệ thống Blind Vow (khế ước và lời thề)

Người chơi có thể lập khế ước hoặc lời thề với: ác quỷ (khế ước), thần linh, tinh linh, giáo hội.

Đề xuất (chưa duyệt chi tiết):
- Mỗi lời thề cho sức mạnh và đòi một cái giá.
- Mỗi đối tượng có phong cách và rủi ro riêng.
- Phá lời thề có hậu quả.
- Class Knight có cơ chế Oath, có thể liên kết.

Chi tiết thiết kế sau khi prototype combat ổn.

## 7. Combat

- Phòng thủ: block, parry, né/dash, đều tốn stamina; có thể có posture và guard break.
- Tấn công: đòn nhẹ, đòn nặng, kỹ năng vũ khí; mỗi đòn có giai đoạn báo hiệu, gây sát thương, hồi phục để đối thủ đọc được và phản công.
- Server quyết định trúng đòn và parry; phải tính đến độ trễ mạng.
- Parry không thắng mọi đòn: đòn mạnh, đòn chộp, cơ chế boss có thể cần cách đối phó khác.
- Con số cụ thể (thời gian parry, stamina, sát thương) chỉnh dần khi có prototype, và đặt trong file config.

## 8. Chết vĩnh viễn và di sản

- Chết là mất nhân vật vĩnh viễn, server quyết định. Chống nhân bản, chống ngắt kết nối để thoát chết, chống xóa nhầm do lỗi lưu.
- Đề xuất (chờ Vinny duyệt): linh hồn người chơi đầu thai thành nhân vật mới sau mỗi lần chết; giữ lại một phần nhỏ "di sản" cấp tài khoản (lore đã khám phá, danh hiệu, ký ức kiếp trước), không tăng sức mạnh quá lớn.

## 9. Lộ trình

**Prototype đầu tiên:** chỉ Human + Warrior, một căn phòng, một thanh kiếm, một con quái, đánh nghe sướng tay.

1. Dựng khung dự án (Rojo, GitHub). *(xong)*
2. Đòn đánh thường, hitbox, thanh máu, một dummy.
3. Block, parry, né, stamina.
4. Quái có AI và đòn báo hiệu.
5. Lưu dữ liệu nhân vật (cẩn thận với chết vĩnh viễn).
6. Boss làng tân thủ.
7. Sau đó mới mở rộng: chủng tộc, class, hệ thống Blind Vow, thế giới, PvP.

## 10. Còn bỏ ngỏ

- Tên boss làng tân thủ, tên NPC bạn đồng hành, ngoại hình Mikami.
- Ai giam chị gái thật và vùng đất đó tên gì (để sau).
- Chi tiết hệ thống Blind Vow, di sản, cân bằng chủng tộc.
- Tài liệu thiết kế gốc nằm trong Claude Docs của Vinny; file này là bản đồng bộ hơn.
