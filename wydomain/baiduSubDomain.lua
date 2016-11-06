local domain = arg[1]
local outfile = arg[2] or "baidu.json"
if type(domain) ~= "string" then
    print("Expect 2 parameter , got", domain, type(domain))
    return
end
--yiguo.com
local x = string.find(domain, "%.")

local urlname = string.sub(domain, 1, x-1)
local suffix = string.sub(domain, x)
local keyword = "site%3A*."..urlname..suffix

-- print(urlname)
-- print(suffix)

local page_start = 1
local page_end = 10

local http = require("socket.http")

--string 2 table
local jsonS2T = require("cjson").decode
--table 2 string
local jsonT2S = require("cjson").encode

local strTime = os.date("%Y-%m-%d_%H:%M:%S", os.time())

local oldTime = os.time();
local newTime = os.time();

local ss = {}

for i=page_start, page_end do
    print(i)
    local pn = (i-1)*10
    local url = "https://www.baidu.com/s?wd="..keyword.."&pn="..pn.."&oq="..keyword.."&ie=utf-8&usm=1&rsv_page=1"
    local b, c, h = http.request(url)
    if c == 200 then
        local pos = 1
        local x, y
        local head = 0
        local tail = 0
        local kw = ""

        while  true do
            kw = 'style="text%-decoration:none;">'
            x, y = string.find(b, kw, pos)
            if x == nil or y == nil then break end
            pos = y + 1
            head = y + 1
            kw = urlname
            x, y = string.find(b, kw, pos)
            if x == nil or y == nil then break end
            pos = y + 1
            tail = y
            local str = string.sub(b, head, tail) 
            if #str >= 30 then
                str = string.gsub(str, "..", "")
                str = string.gsub(str, "...", "")
                str = string.gsub(str, "....", "")
                str = string.gsub(str, ".....", "")
            end
            str = string.gsub(str, "http://", "")
            str = string.gsub(str, "https://", "")
            
            str = str .. suffix
            ss[str] = str
        end
    end
end

local sss = {}
for k,v in pairs(ss) do
    table.insert(sss, v)
end

local out = jsonT2S(sss)

local resultfile = "result"
local file = io.open(resultfile, "rb")
if file then 
    file:close() 
else
    os.execute('mkdir '..resultfile)
end

local file = io.open(resultfile.."/"..domain, "rb")
if file then 
    file:close() 
else
    os.execute('mkdir '..resultfile..'/'..domain)
end

local file = io.open (resultfile.."/"..domain.."/"..outfile, "w")
file:write(out)
file:flush()
file:close()
