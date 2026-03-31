package com.generated.eventtest.event;

import com.generated.eventtest.Eventtest;
import net.minecraftforge.fml.event.lifecycle.FMLCommonSetupEvent;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.player.Player;
import net.minecraftforge.event.ServerChatEvent;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.event.entity.player.PlayerEvent;
import net.minecraftforge.event.level.BlockEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

@Mod.EventBusSubscriber(modid = Eventtest.MOD_ID, bus = Mod.EventBusSubscriber.Bus.FORGE)
public class ModEvents {

    public static void onCommonSetup(FMLCommonSetupEvent event) {
        // Common setup
    }

    @SubscribeEvent
    public static void onPlayerChat(ServerChatEvent event) {

        ServerPlayer player = event.getPlayer();
        var level = player.level();
        var soundPos = player.blockPosition();
        String message = event.getMessage().getString();
    if ("ping" == message) {
        player.sendSystemMessage(Component.literal("pong"));
    }
    }
    @SubscribeEvent
    public static void onPlayerChangeDimension(PlayerEvent.PlayerChangedDimensionEvent event) {

        Player player = event.getEntity();
        var level = player.level();
        var soundPos = player.blockPosition();
    player.sendSystemMessage(Component.literal("changed"));
    }
    @SubscribeEvent
    public static void onServerTick(TickEvent.ServerTickEvent event) {
        if (event.phase != TickEvent.Phase.END) {
            return;
        }
        var server = net.minecraftforge.server.ServerLifecycleHooks.getCurrentServer();

    }
    @SubscribeEvent
    public static void onBlockBreak(BlockEvent.BreakEvent event) {

        Player player = event.getPlayer();
        var level = event.getLevel();
        var pos = event.getPos();
        var state = event.getState();
        var soundPos = pos;
    if (!(level.isClientSide())) {
        player.sendSystemMessage(Component.literal("broke one"));
    }
    }
}
