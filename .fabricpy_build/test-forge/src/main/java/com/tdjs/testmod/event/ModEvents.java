package com.tdjs.testmod.event;

import com.tdjs.testmod.Test;
import net.minecraftforge.fml.event.lifecycle.FMLCommonSetupEvent;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.player.Player;
import net.minecraftforge.event.entity.player.PlayerEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

@Mod.EventBusSubscriber(modid = Test.MOD_ID, bus = Mod.EventBusSubscriber.Bus.FORGE)
public class ModEvents {

    public static void onCommonSetup(FMLCommonSetupEvent event) {
        // Common setup
    }

    @SubscribeEvent
    public static void onPlayerJoin(PlayerEvent.PlayerLoggedInEvent event) {

        Player player = event.getEntity();
        var level = player.level();
        var soundPos = player.blockPosition();
    player.sendSystemMessage(Component.literal("You are running a Development build Of a demo for FabricPy"));
    }
}
