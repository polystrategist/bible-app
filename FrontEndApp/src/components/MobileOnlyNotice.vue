<script lang="ts" setup>
import { NButton } from 'naive-ui';
import { Icon } from '@iconify/vue';
import qrSrc from '../assets/mobile-app-qr.svg';

// Shared "checkout lives in the mobile app" notice.
//
// Web/desktop purchasing (RevenueCat Web Billing / Paddle) is turned off until
// Paddle is verified for production (see `webBillingStore.checkoutEnabled`). In
// the meantime every purchase surface shows this: a QR code to the Play Store
// listing plus a short explanation that subscribing is mobile-only for now.
const PLAY_STORE_URL =
    'https://play.google.com/store/apps/details?id=com.believers.sword.believers_sword_mobile';

function openStore() {
    // Electron: open in the OS browser; web: a normal new tab.
    if (window.isElectron && window.browserWindow?.openExternal) {
        void window.browserWindow.openExternal(PLAY_STORE_URL);
    } else {
        window.open(PLAY_STORE_URL, '_blank', 'noopener');
    }
}
</script>

<template>
    <div class="mobile-only">
        <div class="mobile-only__qr">
            <img
                :src="qrSrc"
                width="148"
                height="148"
                alt="Scan to get Believers Sword on Google Play"
            />
        </div>
        <div class="mobile-only__body">
            <p class="mobile-only__title">
                <Icon icon="mdi:cellphone-arrow-down" /> Subscribe in the mobile app
            </p>
            <p class="mobile-only__text">
                Checkout isn’t available on the desktop or web app yet. For now, the only
                way to subscribe is through the <strong>Believers Sword</strong> mobile app
                — scan the code to get it on Google Play. Your plan works here automatically
                once it’s active.
            </p>
            <NButton size="small" tertiary @click="openStore">
                <template #icon><Icon icon="mdi:google-play" /></template>
                Open Google Play
            </NButton>
        </div>
    </div>
</template>

<style scoped>
/* QR on the left, text + action on the right (stacks on narrow widths). */
.mobile-only {
    display: flex;
    flex-direction: row;
    align-items: center;
    text-align: left;
    gap: 20px;
    padding: 8px 4px;
    max-width: 560px;
    margin: 0 auto;
}
.mobile-only__body {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
    min-width: 0;
}
/* White, padded backing so the QR scans in dark mode too. */
.mobile-only__qr {
    background: #ffffff;
    padding: 12px;
    border-radius: 12px;
    line-height: 0;
    flex-shrink: 0;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.12);
}
.mobile-only__qr img {
    display: block;
    image-rendering: pixelated;
}
.mobile-only__title {
    display: flex;
    align-items: center;
    gap: 6px;
    margin: 0;
    font-weight: 700;
    font-size: 15px;
}
.mobile-only__text {
    margin: 0;
    font-size: 13px;
    line-height: 1.55;
    opacity: 0.8;
}
@media (max-width: 480px) {
    .mobile-only {
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    .mobile-only__body {
        align-items: center;
    }
}
</style>
