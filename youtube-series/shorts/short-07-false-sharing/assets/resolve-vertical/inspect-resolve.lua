local r = Resolve()
local p = r:GetProjectManager():GetCurrentProject()
local f = assert(io.open([[/Users/keremkazan/Documents/Projects/Content HQ/youtube-series/shorts/short-07-false-sharing/assets/resolve-vertical/resolve-settings.txt]], "w"))
f:write("Version: "..r:GetVersionString().."\nProject: "..p:GetName().."\n")
for k,v in pairs(p:GetSetting()) do f:write(k.."="..tostring(v).."\n") end
f:close()
print("SHORT07_INSPECTION_DONE")
