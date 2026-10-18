# Tạo các file animation kiếm (KeyframeSequence cho rig R15) trong assets/roblox/animations.
# Chạy: powershell -ExecutionPolicy Bypass -File tools/animations/Build-SwordAnimations.ps1
#
# Mỗi khớp: góc xoay (độ) quanh trục của khớp, cộng dịch chuyển y (stud) nếu cần.
#   X dương: tay/chân đưa ra trước, thân/đầu ngả ra sau.
#   Y dương: xoay sang trái (nhìn từ trên xuống).
#   Z dương: tay/chân bên phải dang ra ngoài; với bên trái thì dùng số âm.
# Khớp không có trong tư thế thì animation không đụng tới (để animation khác điều khiển).

$ErrorActionPreference = 'Stop'
$outDir = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..\assets\roblox\animations'))

# --- Tay phải cầm kiếm: buông thấp cạnh hông, hơi ra sau, khuỷu hơi cong ---
# (Hướng kiếm trong bàn tay đặt ở WeaponModelConfig: mũi chĩa ra ngoài, ra sau, gần sát đất.)
$hold = @{
	RightUpperArm = @{ rx = -10; ry = 0; rz = 12 }
	RightLowerArm = @{ rx = 15;  ry = 0; rz = 0 }
	RightHand     = @{ rx = 0;   ry = 0; rz = 0 }
}

# --- Tư thế thủ khi đứng yên (theo ảnh tham khảo SwordIdle_01), không gồm tay phải ---
# Chân trụ rộng: chân trái bước lên trước và khuỵu, chân phải lùi và dang ra.
# Thân xoay nhẹ để vai trái ra trước; tay trái co, cẳng tay đưa ra trước.
$idle = @{
	LowerTorso    = @{ rx = 0;  ry = -8;  rz = 0; y = -0.14 }
	UpperTorso    = @{ rx = -4; ry = -4;  rz = 0 }
	Head          = @{ rx = 3;  ry = 12;  rz = 0 }
	LeftUpperArm  = @{ rx = 10; ry = 0;   rz = -20 }
	LeftLowerArm  = @{ rx = 75; ry = 0;   rz = 0 }
	LeftHand      = @{ rx = -10; ry = 0;  rz = 0 }
	LeftUpperLeg  = @{ rx = 35; ry = 0;   rz = -12 }
	LeftLowerLeg  = @{ rx = -40; ry = 0;  rz = 0 }
	LeftFoot      = @{ rx = 5;  ry = 0;   rz = 0 }
	RightUpperLeg = @{ rx = -12; ry = 0;  rz = 14 }
	RightLowerLeg = @{ rx = -26; ry = 0;  rz = 0 }
	RightFoot     = @{ rx = 38; ry = 0;   rz = 0 }
}
# Nhịp thở: ngực nâng nhẹ, tay trái nhích rất ít.
$idleBreath = @{}
foreach ($k in $idle.Keys) { $idleBreath[$k] = $idle[$k].Clone() }
$idleBreath.LowerTorso.y = -0.12
$idleBreath.UpperTorso.rx = -2.5
$idleBreath.Head.rx = 1.5
$idleBreath.LeftUpperArm.rx = 12
$idleBreath.LeftLowerArm.rx = 72

# --- Với tay phải xuống chuôi kiếm ở hông phải (dùng khi rút và tra kiếm) ---
$reach = @{
	RightUpperArm = @{ rx = 5;   ry = 0; rz = -3 }
	RightLowerArm = @{ rx = 80;  ry = 0; rz = 0 }
	RightHand     = @{ rx = -15; ry = 0; rz = 0 }
}

# AnimationPriority: Action = 2, Action2 = 3
$animations = @(
	@{ name = 'SwordHold'; loop = $true; priority = 2; keyframes = @(@{ time = 0; pose = $hold }, @{ time = 1; pose = $hold }) },
	@{ name = 'SwordReadyIdle'; loop = $true; priority = 2; keyframes = @(@{ time = 0; pose = $idle }, @{ time = 1.6; pose = $idleBreath }, @{ time = 3.2; pose = $idle }) },
	@{ name = 'SwordReach'; loop = $false; priority = 3; keyframes = @(@{ time = 0.25; pose = $reach }, @{ time = 0.8; pose = $reach }) }
)

$tree = [ordered]@{
	HumanoidRootPart = [ordered]@{
		LowerTorso = [ordered]@{
			UpperTorso = [ordered]@{
				Head = [ordered]@{}
				RightUpperArm = [ordered]@{ RightLowerArm = [ordered]@{ RightHand = [ordered]@{} } }
				LeftUpperArm = [ordered]@{ LeftLowerArm = [ordered]@{ LeftHand = [ordered]@{} } }
			}
			LeftUpperLeg = [ordered]@{ LeftLowerLeg = [ordered]@{ LeftFoot = [ordered]@{} } }
			RightUpperLeg = [ordered]@{ RightLowerLeg = [ordered]@{ RightFoot = [ordered]@{} } }
		}
	}
}

$inv = [System.Globalization.CultureInfo]::InvariantCulture
function F([double]$v) { [math]::Round($v, 6).ToString('0.######', $inv) }

# CFrame.Angles(x, y, z) = Rx * Ry * Rz
function CFrameXml($j) {
	$d = [math]::PI / 180
	$x = $(if ($j) { $j.rx * $d } else { 0 }); $y = $(if ($j) { $j.ry * $d } else { 0 }); $z = $(if ($j) { $j.rz * $d } else { 0 })
	$cx = [math]::Cos($x); $sx = [math]::Sin($x); $cy = [math]::Cos($y); $sy = [math]::Sin($y); $cz = [math]::Cos($z); $sz = [math]::Sin($z)
	$r = @(
		($cy * $cz), (-$cy * $sz), $sy,
		($cx * $sz + $sx * $sy * $cz), ($cx * $cz - $sx * $sy * $sz), (-$sx * $cy),
		($sx * $sz - $cx * $sy * $cz), ($sx * $cz + $cx * $sy * $sz), ($cx * $cy)
	)
	$py = $(if ($j -and $j.ContainsKey('y')) { $j.y } else { 0 })
	$names = 'R00', 'R01', 'R02', 'R10', 'R11', 'R12', 'R20', 'R21', 'R22'
	$s = "<CoordinateFrame name=`"CFrame`"><X>0</X><Y>$(F $py)</Y><Z>0</Z>"
	for ($i = 0; $i -lt 9; $i++) { $s += "<$($names[$i])>$(F $r[$i])</$($names[$i])>" }
	return $s + '</CoordinateFrame>'
}

# Khớp có trong tư thế, hoặc có khớp con nằm trong tư thế
function Used($name, $children, $pose) {
	if ($pose.ContainsKey($name)) { return $true }
	foreach ($c in $children.Keys) { if (Used $c $children[$c] $pose) { return $true } }
	return $false
}

$script:ref = 0
function NextRef { $script:ref++; return "RBX$($script:ref)" }

function PoseXml($name, $children, $pose) {
	$animated = $pose.ContainsKey($name)
	$s = "<Item class=`"Pose`" referent=`"$(NextRef)`"><Properties>"
	$s += "<string name=`"Name`">$name</string>"
	$s += CFrameXml $pose[$name]
	# PoseEasingStyle.Cubic = 3, PoseEasingDirection.InOut = 2. Khớp chỉ làm đường dẫn: Weight 0.
	$s += "<token name=`"EasingStyle`">3</token><token name=`"EasingDirection`">2</token><float name=`"Weight`">$(if ($animated) { 1 } else { 0 })</float>"
	$s += '</Properties>'
	foreach ($c in $children.Keys) {
		if (Used $c $children[$c] $pose) { $s += PoseXml $c $children[$c] $pose }
	}
	return $s + '</Item>'
}

New-Item -ItemType Directory -Force $outDir | Out-Null
foreach ($anim in $animations) {
	$script:ref = 0
	$xml = '<roblox xmlns:xmime="http://www.w3.org/2005/05/xmlmime" version="4">'
	$xml += "<Item class=`"KeyframeSequence`" referent=`"$(NextRef)`"><Properties>"
	$xml += "<string name=`"Name`">$($anim.name)</string><bool name=`"Loop`">$($anim.loop.ToString().ToLower())</bool><token name=`"Priority`">$($anim.priority)</token>"
	$xml += '</Properties>'
	foreach ($kf in $anim.keyframes) {
		$xml += "<Item class=`"Keyframe`" referent=`"$(NextRef)`"><Properties><string name=`"Name`">Keyframe</string><float name=`"Time`">$(F $kf.time)</float></Properties>"
		foreach ($root in $tree.Keys) { $xml += PoseXml $root $tree[$root] $kf.pose }
		$xml += '</Item>'
	}
	$xml += '</Item></roblox>'
	$path = Join-Path $outDir "$($anim.name).rbxmx"
	[System.IO.File]::WriteAllText($path, $xml, (New-Object System.Text.UTF8Encoding($false)))
	Write-Output "Wrote $path"
}
