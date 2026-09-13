local WorldDonation = "7QAZ"
local WebhookDonation = "https://discord.com/api/webhooks/1277818368967315499/YP-vKWX3EozPvTqRr9GKQkJkxt6sCjjqicjuJthKP9ozW-66k0j-BKqHKED5ebfHRiPT"
local WebhookStatus = "https://discord.com/api/webhooks/1277818368967315499/YP-vKWX3EozPvTqRr9GKQkJkxt6sCjjqicjuJthKP9ozW-66k0j-BKqHKED5ebfHRiPT"
local WebhookStarted = "https://discord.com/api/webhooks/1277818368967315499/YP-vKWX3EozPvTqRr9GKQkJkxt6sCjjqicjuJthKP9ozW-66k0j-BKqHKED5ebfHRiPT"
local StatusMessageID = "1284581891525316609"

local EmojiCrown = "<a:crown:1269973214445178941>"
local EmojiGrowID = "<:growid:1269978167888838681>"
local EmojiProduct = "<a:productdet:1174338594819821639>"
local EmojiBalance = "<a:balance:1287003129790861343>"
local EmojiWorld = "<a:world:1269975957385773156>"
local EmojiMonitor = "<:monitor:1276834635258662952>"

local ColorEmbed = "0x2ecc71"
local UsernameWebhook = "Nexblu Store"
local AvatarWebhook = ""

local bot  = getBot()

function checkBanned()
    while bot.status ~= BotStatus.online or bot:getPing() == 0 do
        bot.auto_reconnect = true
        sleep(5000)
        if bot.status == BotStatus.account_banned then
            bot:stopScript()
        end
    end
end

function reconnect(world,id,x,y)
    if bot.status == BotStatus.online and (bot.x ~= x or bot.y ~= y) then
        local cons = 0
        while bot:getWorld().name ~= world:upper() do
            bot:sendPacket(3,"action|join_request\nname|"..world:upper().."\ninvitedWorld|0")
            sleep(5000)
            if cons == 10 then
                cons = 0
                bot:disconnect()
                sleep(100)
                checkBanned()
            else
                cons = cons + 1
            end
        end
        if id ~= "" and getTile(bot.x,bot.y).fg == 6 then
            bot:sendPacket(3,"action|join_request\nname|"..world:upper().."|"..id:upper().."\ninvitedWorld|0")
            sleep(2000)
            if cons == 10 then
                cons = 0
                bot:disconnect()
                sleep(100)
                checkBanned()
            else
                cons = cons + 1
            end
        end
        if x and y and (bot.x ~= x or bot.y ~= y) then
            bot:findPath(x,y)
            sleep(100)
        end
    end
    if bot.status ~= BotStatus.online or bot:getPing() == 0 then
        checkBanned()
        while bot:getWorld().name ~= world:upper() do
            bot:sendPacket(3,"action|join_request\nname|"..world:upper().."\ninvitedWorld|0")
            sleep(5000)
        end
        if id ~= "" and getTile(bot.x,bot.y).fg == 6 then
            bot:sendPacket(3,"action|join_request\nname|"..world:upper().."|"..id:upper().."\ninvitedWorld|0")
            sleep(2000)
        end
        if x and y and (bot.x ~= x or bot.y ~= y) then
            bot:findPath(x,y)
            sleep(100)
        end
    end
end


function extract_info_dona(str)
    str = str:gsub("%d+%[```", ""):gsub("```%d+%]", "")
    local pattern = "(.*) places `(.*)`` (.*)`` into the (.*)"
    local name, quantity, item, _ = str:match(pattern)
    name = name:sub(3)
    quantity = quantity:sub(2)
    item = item:sub(3)
    return name, quantity, item
end


function extract_info_vend(str)
    str = str:gsub("%d+%[```", ""):gsub("```%d+%]", "")
    print("String after gsub:", str)
    local pattern = "(.*) bought (.*) for (%d+) (.*)%.(.*)"
    local name, item_bought, quantity, item, item_type = str:match(pattern)
    if name then
        name = name:sub(3)
    else
        print("Pattern did not match")
    end
    item = item:gsub("%.", "")
    return name, item_bought, quantity, item, item_type
end

function OnVariantList(variant, netid) -- Using the variantlist event parameters. You can view them from enums.md
    if variant:get(0):getString() == "OnConsoleMessage" and    (variant:get(1):getString():find("into the Donation Box") or variant:get(1):getString():find("bought")) and  (variant:get(1):getString():find("World Lock") or variant:get(1):getString():find("Diamond Lock") or variant:get(1):getString():find("Blue Gem Lock"))  then
        local message = variant:get(1):getString()    

        local webhook = Webhook.new(WebhookDonation)
        webhook.username = UsernameWebhook
        webhook.avatar_url = AvatarWebhook
        webhook.embed1.use = true
        webhook.embed1.color = ColorEmbed
        if message:find("into the Donation Box") and ( not variant:get(1):getString():find("CP")) then
            local name, quantity, item = extract_info_dona(message)
            bot:say("Thanks Sir")
            webhook.embed1.description = "**" .. EmojiCrown .. " Donation Log " .. EmojiCrown .. "\n\n[" .. EmojiGrowID .. "] GrowID : " .. name .. "\n[" .. EmojiBalance .. "] Amount : " .. quantity .. " " .. item .. "**"
            webhook:send()
        elseif message:find("bought") and ( not variant:get(1):getString():find("CP")) then
            local name, item_bought, quantity, item, item_type = extract_info_vend(message)
            bot:say("Thanks Sir")
            webhook.embed1.description = "**" .. EmojiCrown .. " Donation Log " .. EmojiCrown .. "\n\n[" .. EmojiGrowID .. "] GrowID : " .. name .. "\n[" .. EmojiBalance .. "] Amount : " .. quantity .. " " .. item .. "\n[" .. EmojiProduct .. "] Item : " .. item_bought .. "**"
            webhook:send()
        else
            bot:say("Fake Donation")
        end
    end
  end
  addEvent(Event.variantlist, OnVariantList)
  reconnect(WorldDonation,"")
  local webhook = Webhook.new(WebhookStarted)
  webhook.username = UsernameWebhook
  webhook.avatar_url = AvatarWebhook
  webhook.embed1.use = true
  webhook.embed1.color = ColorEmbed
      webhook.embed1.title = bot.name.." <t:"..os.time()..":R>"
      webhook.embed1.description = "**[" .. EmojiGrowID .. "] Bot : "..bot.name.."\n[" .. EmojiWorld .. "] World : ".. WorldDonation .."**"
      webhook.embed1.footer.text = "Start Script"
  webhook:send()
  while bot:getWorld().name:upper() ~= WorldDonation:upper() do
    bot:warp(WorldDonation)
    sleep(8000)
  end

while true do
    if bot.status  == 1 then
    local webhook = Webhook.new(WebhookStatus)
    webhook.username = UsernameWebhook
    webhook.avatar_url = AvatarWebhook
    webhook.embed1.use = true
    webhook.embed1.color = ColorEmbed
        webhook.embed1.title = bot.name .. " <t:".. os.time()..":R>"
        webhook.embed1.description = "**[" .. EmojiGrowID .. "] Bot : "..bot.name.."\n[" .. EmojiWorld .. "] World : "..bot:getWorld().name.."\n[" .. EmojiMonitor .. "] Status : Online**"
    webhook:edit(StatusMessageID)
    else
        local webhook = Webhook.new(WebhookStatus)
        webhook.username = UsernameWebhook
        webhook.avatar_url = AvatarWebhook
        webhook.embed1.use = true
        webhook.embed1.color = ColorEmbed
        webhook.embed1.title = bot.name .. " <t:".. os.time()..":R>"
        webhook.embed1.description = "**[" .. EmojiGrowID .. "] Bot : "..bot.name.."\n[" .. EmojiWorld .. "] World : "..bot:getWorld().name.."\n[" .. EmojiMonitor .. "] Status : Offline**"
        webhook:edit(StatusMessageID)
        reconnect(WorldDonation,"")
    end
    listenEvents(10)
end