"""
API mapping tables: Python ctx.* calls → Java method calls.

The transpiler looks up "ctx.player.send_message" etc. and substitutes
the Java equivalent. {0}, {1} are positional args; named kwargs are also supported.

Fabric targets MC 1.20.1 / Fabric API 0.91+
Forge targets MC 1.20.1 / Forge 47+
"""

# ── Fabric API map ────────────────────────────────────────────────────────── #

FABRIC_API_MAP: dict[str, str] = {
    # Player
    "ctx.player":
        'player',
    "ctx.player.send_message":
        'player.sendMessage(Text.literal({0}), false)',
    "ctx.player.send_action_bar":
        'player.sendMessage(Text.literal({0}), true)',
    "ctx.player.teleport":
        '((ServerPlayerEntity)player).teleport((ServerWorld)world, {0}, {1}, {2}, Set.of(), player.getYaw(), player.getPitch())',
    "ctx.player.teleport_dimension":
        'player.getServer().getCommandManager().executeWithPrefix(player.getCommandSource().withSilent(), "execute in " + {0} + " run tp " + player.getName().getString() + " " + {1} + " " + {2} + " " + {3})',
    "ctx.player.give_item":
        'player.giveItemStack(new ItemStack(Registries.ITEM.get(new Identifier({0})), {1}))',
    "ctx.player.remove_item":
        'player.getServer().getCommandManager().executeWithPrefix(player.getCommandSource().withSilent(), "clear " + player.getName().getString() + " " + {0} + " " + ((int)({1})))',
    "ctx.player.get_health":
        'player.getHealth()',
    "ctx.player.set_health":
        'player.setHealth({0})',
    "ctx.player.is_creative":
        'player.isCreative()',
    "ctx.player.is_sneaking":
        'player.isSneaking()',
    "ctx.player.is_sprinting":
        'player.isSprinting()',
    "ctx.player.get_name":
        'player.getName().getString()',
    "ctx.player.set_on_fire":
        'player.setFireTicks((int)({0} * 20))',
    "ctx.player.heal":
        'player.heal({0})',
    "ctx.player.damage":
        'player.damage(world.getDamageSources().generic(), {0})',
    "ctx.player.add_effect":
        'player.addStatusEffect(new StatusEffectInstance(Registries.STATUS_EFFECT.get(new Identifier(({0}).contains(":") ? {0} : "minecraft:" + ({0}).toLowerCase())), {1} * 20, {2}))',
    "ctx.player.remove_effect":
        'player.removeStatusEffect(Registries.STATUS_EFFECT.get(new Identifier(({0}).contains(":") ? {0} : "minecraft:" + ({0}).toLowerCase())))',
    "ctx.player.clear_effects":
        'player.clearStatusEffects()',
    "ctx.player.get_hunger":
        'player.getHungerManager().getFoodLevel()',
    "ctx.player.set_hunger":
        'player.getHungerManager().setFoodLevel((int)({0}))',
    "ctx.player.get_saturation":
        'player.getHungerManager().getSaturationLevel()',
    "ctx.player.set_saturation":
        'player.getHungerManager().setSaturationLevel((float)({0}))',
    "ctx.player.add_experience":
        'player.addExperience((int)({0}))',
    "ctx.player.kill":
        'player.kill()',
    "ctx.player.get_pos_x":
        'player.getX()',
    "ctx.player.get_pos_y":
        'player.getY()',
    "ctx.player.get_pos_z":
        'player.getZ()',

    # World
    "ctx.world":
        'world',
    "ctx.world.is_client":
        'world.isClient()',
    "ctx.world.play_sound":
        'Registries.SOUND_EVENT.getOrEmpty(new Identifier({0})).ifPresent(s -> world.playSound(null, soundPos, s, SoundCategory.BLOCKS, {1}, {2}))',
    "ctx.world.explode":
        'world.createExplosion(null, {0}, {1}, {2}, {3}, false, World.ExplosionSourceType.NONE)',
    "ctx.world.set_block":
        'world.setBlockState(new BlockPos((int){0}, (int){1}, (int){2}), Registries.BLOCK.get(new Identifier({3})).getDefaultState())',
    "ctx.world.set_block_in_dimension":
        'world.getServer().getCommandManager().executeWithPrefix(world.getServer().getCommandSource().withSilent(), "execute in " + {0} + " run setblock " + ((int)({1})) + " " + ((int)({2})) + " " + ((int)({3})) + " " + {4})',
    "ctx.world.fill_in_dimension":
        'world.getServer().getCommandManager().executeWithPrefix(world.getServer().getCommandSource().withSilent(), "execute in " + {0} + " run fill " + ((int)({1})) + " " + ((int)({2})) + " " + ((int)({3})) + " " + ((int)({4})) + " " + ((int)({5})) + " " + ((int)({6})) + " " + {7} + ({8} != null ? " " + {8} : ""))',
    "ctx.world.place_structure":
        'world.getServer().getCommandManager().executeWithPrefix(world.getServer().getCommandSource().withSilent(), "execute in " + {0} + " run place template " + {1} + " " + ((int)({2})) + " " + ((int)({3})) + " " + ((int)({4})))',
    "ctx.world.place_nbt":
        'world.getServer().getCommandManager().executeWithPrefix(world.getServer().getCommandSource().withSilent(), "execute in " + {0} + " run place template " + {1} + " " + ((int)({2})) + " " + ((int)({3})) + " " + ((int)({4})))',
    "ctx.world.get_time":
        'world.getTime()',
    "ctx.world.is_day":
        '(world.getTimeOfDay() % 24000L < 13000L)',
    "ctx.world.is_raining":
        'world.isRaining()',
    "ctx.world.get_dimension":
        'world.getRegistryKey().getValue().toString()',
    "ctx.world.spawn_lightning":
        'world.spawnEntity(new LightningEntity(EntityType.LIGHTNING_BOLT, world))',

    # Context values
    "ctx.pos":
        'pos',
    "ctx.state":
        'state',
    "ctx.hand":
        'hand',
    "ctx.stack":
        'stack',
    "ctx.message":
        'message',
    "ctx.server":
        'server',
    "ctx.server.run_command":
        'server.getCommandManager().executeWithPrefix(server.getCommandSource().withSilent(), {0})',
    "ctx.server.reload_data":
        'server.getCommandManager().executeWithPrefix(server.getCommandSource().withSilent(), "reload")',

    # Source (commands)
    "ctx.source":
        'context.getSource()',
    "ctx.source.send_message":
        'context.getSource().sendFeedback(() -> Text.literal({0}), false)',
    "ctx.source.get_player":
        'context.getSource().getPlayer()',
    "ctx.source.get_pos":
        'context.getSource().getPosition()',
    "ctx.source.run_command":
        'context.getSource().getServer().getCommandManager().executeWithPrefix(context.getSource().withSilent(), {0})',
}

# ── Required Java imports for Fabric ─────────────────────────────────────── #

FABRIC_EXTRA_IMPORTS: list[str] = [
    "import net.minecraft.text.Text;",
    "import net.minecraft.registry.Registries;",
    "import net.minecraft.util.Identifier;",
    "import net.minecraft.item.ItemStack;",
    "import net.minecraft.entity.effect.StatusEffectInstance;",
    "import net.minecraft.entity.effect.StatusEffects;",
    "import net.minecraft.sound.SoundCategory;",
    "import net.minecraft.sound.SoundEvents;",
    "import net.minecraft.server.network.ServerPlayerEntity;",
    "import net.minecraft.server.world.ServerWorld;",
    "import net.minecraft.world.World;",
    "import net.minecraft.util.math.BlockPos;",
    "import java.util.Set;",
]

# ── Forge API map ─────────────────────────────────────────────────────────── #

FORGE_API_MAP: dict[str, str] = {
    # Player
    "ctx.player":
        'player',
    "ctx.player.send_message":
        'player.sendSystemMessage(Component.literal({0}))',
    "ctx.player.send_action_bar":
        'player.displayClientMessage(Component.literal({0}), true)',
    "ctx.player.teleport":
        '((ServerPlayer)player).teleportTo((ServerLevel)level, {0}, {1}, {2}, player.getYRot(), player.getXRot())',
    "ctx.player.teleport_dimension":
        'player.getServer().getCommands().performPrefixedCommand(player.createCommandSourceStack().withSuppressedOutput(), "execute in " + {0} + " run tp " + player.getGameProfile().getName() + " " + {1} + " " + {2} + " " + {3})',
    "ctx.player.give_item":
        'player.addItem(new ItemStack(ForgeRegistries.ITEMS.getValue(new ResourceLocation({0})), {1}))',
    "ctx.player.remove_item":
        'player.getServer().getCommands().performPrefixedCommand(player.createCommandSourceStack().withSuppressedOutput(), "clear " + player.getGameProfile().getName() + " " + {0} + " " + ((int)({1})))',
    "ctx.player.get_health":
        'player.getHealth()',
    "ctx.player.set_health":
        'player.setHealth({0})',
    "ctx.player.is_creative":
        'player.isCreative()',
    "ctx.player.is_sneaking":
        'player.isCrouching()',
    "ctx.player.is_sprinting":
        'player.isSprinting()',
    "ctx.player.get_name":
        'player.getName().getString()',
    "ctx.player.set_on_fire":
        'player.setRemainingFireTicks((int)({0} * 20))',
    "ctx.player.heal":
        'player.heal({0})',
    "ctx.player.damage":
        'player.hurt(level.damageSources().generic(), {0})',
    "ctx.player.add_effect":
        'player.addEffect(new MobEffectInstance(ForgeRegistries.MOB_EFFECTS.getValue(new ResourceLocation(({0}).contains(":") ? {0} : "minecraft:" + ({0}).toLowerCase())), {1} * 20, {2}))',
    "ctx.player.remove_effect":
        'player.removeEffect(ForgeRegistries.MOB_EFFECTS.getValue(new ResourceLocation(({0}).contains(":") ? {0} : "minecraft:" + ({0}).toLowerCase())))',
    "ctx.player.clear_effects":
        'player.removeAllEffects()',
    "ctx.player.get_hunger":
        'player.getFoodData().getFoodLevel()',
    "ctx.player.set_hunger":
        'player.getFoodData().setFoodLevel((int)({0}))',
    "ctx.player.get_saturation":
        'player.getFoodData().getSaturationLevel()',
    "ctx.player.set_saturation":
        'player.getFoodData().setSaturation((float)({0}))',
    "ctx.player.add_experience":
        'player.giveExperiencePoints((int)({0}))',
    "ctx.player.kill":
        'player.kill()',
    "ctx.player.get_pos_x":
        'player.getX()',
    "ctx.player.get_pos_y":
        'player.getY()',
    "ctx.player.get_pos_z":
        'player.getZ()',

    # World (Forge calls it "level" not "world")
    "ctx.world":
        'level',
    "ctx.world.is_client":
        'level.isClientSide()',
    "ctx.world.play_sound":
        'level.playSound(null, soundPos, ForgeRegistries.SOUND_EVENTS.getValue(new ResourceLocation({0})), SoundSource.BLOCKS, {1}, {2})',
    "ctx.world.explode":
        'level.explode(null, {0}, {1}, {2}, {3}, false, Level.ExplosionInteraction.NONE)',
    "ctx.world.set_block":
        'level.setBlock(new BlockPos((int){0}, (int){1}, (int){2}), ForgeRegistries.BLOCKS.getValue(new ResourceLocation({3})).defaultBlockState(), 3)',
    "ctx.world.set_block_in_dimension":
        'level.getServer().getCommands().performPrefixedCommand(level.getServer().createCommandSourceStack().withSuppressedOutput(), "execute in " + {0} + " run setblock " + ((int)({1})) + " " + ((int)({2})) + " " + ((int)({3})) + " " + {4})',
    "ctx.world.fill_in_dimension":
        'level.getServer().getCommands().performPrefixedCommand(level.getServer().createCommandSourceStack().withSuppressedOutput(), "execute in " + {0} + " run fill " + ((int)({1})) + " " + ((int)({2})) + " " + ((int)({3})) + " " + ((int)({4})) + " " + ((int)({5})) + " " + ((int)({6})) + " " + {7} + ({8} != null ? " " + {8} : ""))',
    "ctx.world.place_structure":
        'level.getServer().getCommands().performPrefixedCommand(level.getServer().createCommandSourceStack().withSuppressedOutput(), "execute in " + {0} + " run place template " + {1} + " " + ((int)({2})) + " " + ((int)({3})) + " " + ((int)({4})))',
    "ctx.world.place_nbt":
        'level.getServer().getCommands().performPrefixedCommand(level.getServer().createCommandSourceStack().withSuppressedOutput(), "execute in " + {0} + " run place template " + {1} + " " + ((int)({2})) + " " + ((int)({3})) + " " + ((int)({4})))',
    "ctx.world.get_time":
        'level.getGameTime()',
    "ctx.world.is_day":
        '(level.getDayTime() % 24000L < 13000L)',
    "ctx.world.is_raining":
        'level.isRaining()',
    "ctx.world.get_dimension":
        'level.dimension().location().toString()',

    # Context values
    "ctx.pos":
        'pos',
    "ctx.state":
        'state',
    "ctx.hand":
        'hand',
    "ctx.stack":
        'stack',
    "ctx.message":
        'message',
    "ctx.server":
        'server',
    "ctx.server.run_command":
        'server.getCommands().performPrefixedCommand(server.createCommandSourceStack().withSuppressedOutput(), {0})',
    "ctx.server.reload_data":
        'server.getCommands().performPrefixedCommand(server.createCommandSourceStack().withSuppressedOutput(), "reload")',

    # Source (commands)
    "ctx.source":
        'context.getSource()',
    "ctx.source.send_message":
        'context.getSource().sendSuccess(() -> Component.literal({0}), false)',
    "ctx.source.get_player":
        'context.getSource().getPlayerOrException()',
    "ctx.source.get_pos":
        'context.getSource().getPosition()',
    "ctx.source.run_command":
        'context.getSource().getServer().getCommands().performPrefixedCommand(context.getSource().withSuppressedOutput(), {0})',
}

# ── Required Java imports for Forge ──────────────────────────────────────── #

FORGE_EXTRA_IMPORTS: list[str] = [
    "import net.minecraft.network.chat.Component;",
    "import net.minecraft.resources.ResourceLocation;",
    "import net.minecraft.world.item.ItemStack;",
    "import net.minecraft.world.effect.MobEffectInstance;",
    "import net.minecraft.world.effect.MobEffects;",
    "import net.minecraft.sounds.SoundSource;",
    "import net.minecraft.sounds.SoundEvents;",
    "import net.minecraft.server.level.ServerPlayer;",
    "import net.minecraft.server.level.ServerLevel;",
    "import net.minecraft.world.level.Level;",
    "import net.minecraft.core.BlockPos;",
    "import net.minecraftforge.registries.ForgeRegistries;",
]

# ── Event name mappings ───────────────────────────────────────────────────── #

FABRIC_EVENT_MAP: dict[str, dict] = {
    "player_join": {
        "import": "import net.fabricmc.fabric.api.networking.v1.ServerPlayConnectionEvents;",
        "register": "ServerPlayConnectionEvents.JOIN.register((handler, sender, server) -> {{\n            ServerPlayerEntity player = handler.getPlayer();\n            ServerWorld world = player.getServerWorld();\n            BlockPos soundPos = player.getBlockPos();\n            {body}\n        }});",
    },
    "player_leave": {
        "import": "import net.fabricmc.fabric.api.networking.v1.ServerPlayConnectionEvents;",
        "register": "ServerPlayConnectionEvents.DISCONNECT.register((handler, server) -> {{\n            ServerPlayerEntity player = handler.getPlayer();\n            ServerWorld world = player.getServerWorld();\n            BlockPos soundPos = player.getBlockPos();\n            {body}\n        }});",
    },
    "server_start": {
        "import": "import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;",
        "register": "ServerLifecycleEvents.SERVER_STARTED.register((server) -> {{\n            {body}\n        }});",
    },
    "server_stop": {
        "import": "import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;",
        "register": "ServerLifecycleEvents.SERVER_STOPPING.register((server) -> {{\n            {body}\n        }});",
    },
    "server_tick": {
        "import": "import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;",
        "register": "ServerTickEvents.END_SERVER_TICK.register((server) -> {{\n            {body}\n        }});",
    },
    "block_break": {
        "import": "import net.fabricmc.fabric.api.event.player.PlayerBlockBreakEvents;",
        "register": "PlayerBlockBreakEvents.AFTER.register((world, player, pos, state, be) -> {{\n            var server = world.getServer();\n            BlockPos soundPos = pos;\n            {body}\n        }});",
    },
    "player_respawn": {
        "import": "import net.fabricmc.fabric.api.entity.event.v1.ServerPlayerEvents;",
        "register": "ServerPlayerEvents.AFTER_RESPAWN.register((oldPlayer, newPlayer, alive) -> {{\n            ServerPlayerEntity player = newPlayer;\n            var server = player.getServer();\n            ServerWorld world = player.getServerWorld();\n            BlockPos soundPos = player.getBlockPos();\n            {body}\n        }});",
    },
    "player_death": {
        "import": "import net.fabricmc.fabric.api.entity.event.v1.ServerLivingEntityEvents;",
        "register": "ServerLivingEntityEvents.AFTER_DEATH.register((entity, damageSource) -> {{\n            if (entity instanceof ServerPlayerEntity player) {{\n                var server = player.getServer();\n                ServerWorld world = player.getServerWorld();\n                BlockPos soundPos = player.getBlockPos();\n                {body}\n            }\n        }});",
    },
    "player_change_dimension": {
        "import": "import net.fabricmc.fabric.api.entity.event.v1.ServerEntityWorldChangeEvents;",
        "register": "ServerEntityWorldChangeEvents.AFTER_PLAYER_CHANGE_WORLD.register((player, origin, destination) -> {{\n            var server = player.getServer();\n            ServerWorld world = destination;\n            BlockPos soundPos = player.getBlockPos();\n            {body}\n        }});",
    },
    "player_chat": {
        "import": "import net.fabricmc.fabric.api.message.v1.ServerMessageEvents;",
        "register": "ServerMessageEvents.CHAT_MESSAGE.register((signedMessage, player, params) -> {{\n            var server = player.getServer();\n            ServerWorld world = player.getServerWorld();\n            BlockPos soundPos = player.getBlockPos();\n            String message = signedMessage.getSignedContent();\n            {body}\n        }});",
    },
}

FORGE_EVENT_MAP: dict[str, dict] = {
    "player_join": {
        "class": "PlayerEvent.PlayerLoggedInEvent",
        "import": "import net.minecraftforge.event.entity.player.PlayerEvent;",
        "locals": [
            "        Player player = event.getEntity();",
            "        var server = player.getServer();",
            "        var level = player.level();",
            "        var soundPos = player.blockPosition();",
        ],
    },
    "player_leave": {
        "class": "PlayerEvent.PlayerLoggedOutEvent",
        "import": "import net.minecraftforge.event.entity.player.PlayerEvent;",
        "locals": [
            "        Player player = event.getEntity();",
            "        var server = player.getServer();",
            "        var level = player.level();",
            "        var soundPos = player.blockPosition();",
        ],
    },
    "server_start": {
        "class": "ServerStartedEvent",
        "import": "import net.minecraftforge.event.server.ServerStartedEvent;",
        "locals": [
            "        var server = event.getServer();",
        ],
    },
    "server_stop": {
        "class": "ServerStoppingEvent",
        "import": "import net.minecraftforge.event.server.ServerStoppingEvent;",
        "locals": [
            "        var server = event.getServer();",
        ],
    },
    "server_tick": {
        "class": "TickEvent.ServerTickEvent",
        "import": "import net.minecraftforge.event.TickEvent;",
        "setup": "        if (event.phase != TickEvent.Phase.END) {\n            return;\n        }",
        "locals": [
            "        var server = net.minecraftforge.server.ServerLifecycleHooks.getCurrentServer();",
        ],
    },
    "block_break": {
        "class": "BlockEvent.BreakEvent",
        "import": "import net.minecraftforge.event.level.BlockEvent;",
        "locals": [
            "        Player player = event.getPlayer();",
            "        var level = event.getLevel();",
            "        var server = level.getServer();",
            "        var pos = event.getPos();",
            "        var state = event.getState();",
            "        var soundPos = pos;",
        ],
    },
    "player_respawn": {
        "class": "PlayerEvent.PlayerRespawnEvent",
        "import": "import net.minecraftforge.event.entity.player.PlayerEvent;",
        "locals": [
            "        Player player = event.getEntity();",
            "        var server = player.getServer();",
            "        var level = player.level();",
            "        var soundPos = player.blockPosition();",
        ],
    },
    "player_death": {
        "class": "LivingDeathEvent",
        "import": "import net.minecraftforge.event.entity.living.LivingDeathEvent;",
        "setup": "        if (!(event.getEntity() instanceof Player player)) {\n            return;\n        }",
        "locals": [
            "        var server = player.getServer();",
            "        var level = player.level();",
            "        var soundPos = player.blockPosition();",
        ],
    },
    "player_change_dimension": {
        "class": "PlayerEvent.PlayerChangedDimensionEvent",
        "import": "import net.minecraftforge.event.entity.player.PlayerEvent;",
        "locals": [
            "        Player player = event.getEntity();",
            "        var server = player.getServer();",
            "        var level = player.level();",
            "        var soundPos = player.blockPosition();",
        ],
    },
    "player_chat": {
        "class": "ServerChatEvent",
        "import": "import net.minecraftforge.event.ServerChatEvent;",
        "locals": [
            "        ServerPlayer player = event.getPlayer();",
            "        var server = player.getServer();",
            "        var level = player.level();",
            "        var soundPos = player.blockPosition();",
            "        String message = event.getMessage().getString();",
        ],
    },
}


NEOFORGE_API_MAP: dict[str, str] = {
    **FORGE_API_MAP,
    "ctx.player.give_item":
        'player.addItem(new ItemStack(BuiltInRegistries.ITEM.getValue(ResourceLocation.parse({0})), {1}))',
    "ctx.player.add_effect":
        'player.addEffect(new MobEffectInstance(BuiltInRegistries.MOB_EFFECT.getValue(ResourceLocation.parse((({0}).contains(":") ? {0} : "minecraft:" + ({0}).toLowerCase()))), {1} * 20, {2}))',
    "ctx.player.remove_effect":
        'player.removeEffect(BuiltInRegistries.MOB_EFFECT.getValue(ResourceLocation.parse((({0}).contains(":") ? {0} : "minecraft:" + ({0}).toLowerCase()))))',
    "ctx.world.play_sound":
        'level.playSound(null, soundPos, BuiltInRegistries.SOUND_EVENT.getValue(ResourceLocation.parse({0})), SoundSource.BLOCKS, {1}, {2})',
    "ctx.world.set_block":
        'level.setBlock(new BlockPos((int){0}, (int){1}, (int){2}), BuiltInRegistries.BLOCK.getValue(ResourceLocation.parse({3})).defaultBlockState(), 3)',
}

NEOFORGE_EXTRA_IMPORTS: list[str] = [
    "import net.minecraft.network.chat.Component;",
    "import net.minecraft.resources.ResourceLocation;",
    "import net.minecraft.world.item.ItemStack;",
    "import net.minecraft.world.effect.MobEffectInstance;",
    "import net.minecraft.sounds.SoundSource;",
    "import net.minecraft.sounds.SoundEvents;",
    "import net.minecraft.server.level.ServerPlayer;",
    "import net.minecraft.server.level.ServerLevel;",
    "import net.minecraft.world.level.Level;",
    "import net.minecraft.core.BlockPos;",
    "import net.minecraft.core.registries.BuiltInRegistries;",
]

NEOFORGE_EVENT_MAP: dict[str, dict] = {
    "player_join": {
        "class": "PlayerEvent.PlayerLoggedInEvent",
        "import": "import net.neoforged.neoforge.event.entity.player.PlayerEvent;",
        "locals": [
            "        Player player = event.getEntity();",
            "        var server = player.getServer();",
            "        var level = player.level();",
            "        var soundPos = player.blockPosition();",
        ],
    },
    "player_leave": {
        "class": "PlayerEvent.PlayerLoggedOutEvent",
        "import": "import net.neoforged.neoforge.event.entity.player.PlayerEvent;",
        "locals": [
            "        Player player = event.getEntity();",
            "        var server = player.getServer();",
            "        var level = player.level();",
            "        var soundPos = player.blockPosition();",
        ],
    },
    "server_start": {
        "class": "ServerStartedEvent",
        "import": "import net.neoforged.neoforge.event.server.ServerStartedEvent;",
        "locals": [
            "        var server = event.getServer();",
        ],
    },
    "server_stop": {
        "class": "ServerStoppingEvent",
        "import": "import net.neoforged.neoforge.event.server.ServerStoppingEvent;",
        "locals": [
            "        var server = event.getServer();",
        ],
    },
    "server_tick": {
        "class": "ServerTickEvent.Post",
        "import": "import net.neoforged.neoforge.event.tick.ServerTickEvent;",
        "locals": [
            "        var server = event.getServer();",
        ],
    },
    "block_break": {
        "class": "BlockEvent.BreakEvent",
        "import": "import net.neoforged.neoforge.event.level.BlockEvent;",
        "locals": [
            "        Player player = event.getPlayer();",
            "        var level = event.getLevel();",
            "        var server = level.getServer();",
            "        var pos = event.getPos();",
            "        var state = event.getState();",
            "        var soundPos = pos;",
        ],
    },
    "player_respawn": {
        "class": "PlayerEvent.PlayerRespawnEvent",
        "import": "import net.neoforged.neoforge.event.entity.player.PlayerEvent;",
        "locals": [
            "        Player player = event.getEntity();",
            "        var server = player.getServer();",
            "        var level = player.level();",
            "        var soundPos = player.blockPosition();",
        ],
    },
    "player_death": {
        "class": "LivingDeathEvent",
        "import": "import net.neoforged.neoforge.event.entity.living.LivingDeathEvent;",
        "setup": "        if (!(event.getEntity() instanceof Player player)) {\n            return;\n        }",
        "locals": [
            "        var server = player.getServer();",
            "        var level = player.level();",
            "        var soundPos = player.blockPosition();",
        ],
    },
    "player_change_dimension": {
        "class": "PlayerEvent.PlayerChangedDimensionEvent",
        "import": "import net.neoforged.neoforge.event.entity.player.PlayerEvent;",
        "locals": [
            "        Player player = event.getEntity();",
            "        var server = player.getServer();",
            "        var level = player.level();",
            "        var soundPos = player.blockPosition();",
        ],
    },
    "player_chat": {
        "class": "ServerChatEvent",
        "import": "import net.neoforged.neoforge.event.ServerChatEvent;",
        "locals": [
            "        ServerPlayer player = event.getPlayer();",
            "        var server = player.getServer();",
            "        var level = player.level();",
            "        var soundPos = player.blockPosition();",
            "        String message = event.getRawText();",
        ],
    },
}
