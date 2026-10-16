--!strict
-- Nạp animation của vũ khí cho Animator của nhân vật.
-- Dùng ID đã publish nếu có; nếu chưa, khi test trong Studio thì tạo ID tạm từ KeyframeSequence trong repo.

local AnimationClipProvider = game:GetService("AnimationClipProvider")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local WeaponAnimationConfig = require(Shared:WaitForChild("Config"):WaitForChild("WeaponAnimationConfig"))

local AnimationLoader = {}

local studioIds: { [string]: string } = {}

local function resolveId(ref: WeaponAnimationConfig.AnimationRef): string?
	if ref.id ~= "" then
		return ref.id
	end
	if studioIds[ref.name] then
		return studioIds[ref.name]
	end
	if not RunService:IsStudio() then
		warn(`[AnimationLoader] {ref.name} chưa được publish: điền id trong WeaponAnimationConfig.`)
		return nil
	end

	local assets = ReplicatedStorage:FindFirstChild("Assets")
	local animations = assets and assets:FindFirstChild("Animations")
	local sequence = animations and animations:FindFirstChild(ref.name)
	if not sequence or not sequence:IsA("KeyframeSequence") then
		warn(`[AnimationLoader] Không tìm thấy ReplicatedStorage.Assets.Animations.{ref.name}.`)
		return nil
	end
	local ok, result = pcall(function(): string
		return AnimationClipProvider:RegisterAnimationClip(sequence)
	end)
	if not ok then
		warn(`[AnimationLoader] Không tạo được ID tạm cho {ref.name}: {result}`)
		return nil
	end
	studioIds[ref.name] = result
	return result
end

function AnimationLoader.load(animator: Animator, ref: WeaponAnimationConfig.AnimationRef): AnimationTrack?
	local id = resolveId(ref)
	if not id then
		return nil
	end
	local animation = Instance.new("Animation")
	animation.Name = ref.name
	animation.AnimationId = id
	local track = animator:LoadAnimation(animation)
	return track
end

return AnimationLoader
