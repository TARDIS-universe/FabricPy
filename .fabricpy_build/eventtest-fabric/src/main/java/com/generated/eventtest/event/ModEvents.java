package com.generated.eventtest.event;

import java.util.Set;
import net.fabricmc.fabric.api.entity.event.v1.ServerEntityWorldChangeEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.fabricmc.fabric.api.event.player.PlayerBlockBreakEvents;
import net.fabricmc.fabric.api.message.v1.ServerMessageEvents;
import net.minecraft.item.ItemStack;
import net.minecraft.registry.Registries;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.SoundCategory;
import net.minecraft.sound.SoundEvents;
import net.minecraft.text.Text;
import net.minecraft.util.Identifier;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.World;

/**
 * Event registrations for Event Test.
 */
public class ModEvents {

    public static void register() {
        ServerMessageEvents.CHAT_MESSAGE.register((signedMessage, player, params) -> {
            ServerWorld world = player.getServerWorld();
            BlockPos soundPos = player.getBlockPos();
            String message = signedMessage.getSignedContent();
            if ("ping" == message) {
        player.sendMessage(Text.literal("pong"), false);
    }
        });
        ServerEntityWorldChangeEvents.AFTER_PLAYER_CHANGE_WORLD.register((player, origin, destination) -> {
            ServerWorld world = destination;
            BlockPos soundPos = player.getBlockPos();
            player.sendMessage(Text.literal("changed"), false);
        });
        ServerTickEvents.END_SERVER_TICK.register((server) -> {
            
        });
        PlayerBlockBreakEvents.AFTER.register((world, player, pos, state, be) -> {
            BlockPos soundPos = pos;
            if (!(world.isClient())) {
        player.sendMessage(Text.literal("broke one"), false);
    }
        });
    }
}
