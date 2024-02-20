<template>
    <title>Home</title>
    <div class="container m-auto">
        <div>
            <div class="items-center flex flex-wrap">
                <div class="w-full lg:w-8/12 px-4 ml-auto mr-auto text-center">
                    <div class="p-8 rounded-md faze">
                        <h1 class="text-2xl font-bold">Demo Project For Savannah Informatics</h1>
                        <br>
                        <span class="font-bold">FrontEnd Built Using:</span>
                        <ul>
                            <li>NuxtJS (Vue)</li>
                            <li>TailwindCSS</li>
                            <li>TypeScript (JS)</li>
                        </ul>
                        <br>
                        <span class="font-bold">Backend Built Using:</span>
                        <ul>
                            <li>Python</li>
                            <li>Django</li>
                            <li>Django Rest Framework</li>
                        </ul>
                        <br>
                        <span class="font-bold">Database:</span>
                        <ul>
                            <li>SQLite (For Demo Purposes)</li>
                        </ul>
                        <NuxtLink :to="userIsAuthenticated() ? '/store' : '/login?redirect=/store'"
                            style="display: block; width: fit-content; margin: 1rem auto;"
                            class="bg-emerald-500 text-white active:bg-gray-100 text-sm font-bold uppercase px-6 py-3 rounded shadow hover:shadow-lg outline-none focus:outline-none hover:bg-slate-300 hover:text-slate-900 transition-all duration-500 ease-in-out mt-4">
                            Get
                            Started
                        </NuxtLink>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>