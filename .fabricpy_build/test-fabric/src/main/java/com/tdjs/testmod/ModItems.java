package com.tdjs.testmod;

import net.minecraft.item.Item;
import net.minecraft.item.ItemGroups;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import net.minecraft.util.Identifier;
import net.fabricmc.fabric.api.itemgroup.v1.ItemGroupEvents;
import com.tdjs.testmod.item.pickle;

/**
 * Registers all items for Test Mod.
 */
public class ModItems {
    public static final pickle PICKLE = register("pickle", new pickle());

    private static <T extends Item> T register(String id, T item) {
        return Registry.register(Registries.ITEM, new Identifier(Test.MOD_ID, id), item);
    }

    public static void register() {
        // Items registered via static fields above.
        ItemGroupEvents.modifyEntriesEvent(ItemGroups.INGREDIENTS).register(entries -> entries.add(PICKLE));
    }
}
