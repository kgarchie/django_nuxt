<template>
    <Title>Orders</Title>
    <div class="container mx-auto p-4">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div v-for="item in items" :key="item.id" class="bg-white p-4 rounded-lg border border-gray-200"
                style="max-width: 330px;">
                <img :src="`${$config.public.apiBase}${item.product.image}`" alt=""
                    class="w-full h-40 object-cover rounded-lg">
                <div class="mt-4">
                    <h3 class="text-lg font-semibold" style="text-transform: capitalize;">{{ item.product.name }}</h3>
                    <p class="text-sm text-gray-500">{{ new Date(item.time).toDateString() }}</p>
                    <div class="flex justify-between items-center mt-4">
                        <p class="text-lg font-bold">{{ item.price }}</p>
                        <p class="text-amber-500">{{ item.status }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
import type { APIResponse } from '~/typings';

definePageMeta({
    layout: 'dash'
})

const { body: items } = await $fetch<APIResponse>($config.public.apiBase + '/api/orders', {
    method: 'GET',
    headers: {
        'Authorization': 'Bearer ' + getAuthToken() || ''
    },
    onRequestError(error) {
        console.error(error)
    }
})

console.log(items)
</script>