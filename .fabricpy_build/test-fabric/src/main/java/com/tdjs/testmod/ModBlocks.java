package com.tdjs.testmod;

import net.minecraft.block.Block;
import net.minecraft.item.BlockItem;
import net.minecraft.item.Item;
import net.minecraft.item.ItemGroups;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import net.minecraft.util.Identifier;
import net.fabricmc.fabric.api.itemgroup.v1.ItemGroupEvents;
import com.tdjs.testmod.block.block;

/**
 * Registers all blocks for Test Mod.
 */
public class ModBlocks {
    public static final block BLOCK = register("block", new block());

    private static <T extends Block> T register(String id, T block) {
        Registry.register(Registries.BLOCK, new Identifier(Test.MOD_ID, id), block);
        return block;
    }

    public static void register() {
        // Blocks are registered via static initializer above.
        // Register block items:
        Registry.register(Registries.ITEM, new Identifier(Test.MOD_ID, "block"), new BlockItem(BLOCK, new Item.Settings()));
        ItemGroupEvents.modifyEntriesEvent(ItemGroups.BUILDING_BLOCKS).register(entries -> entries.add(BLOCK));
    }
}
