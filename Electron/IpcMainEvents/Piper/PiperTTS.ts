import { ipcMain, BrowserWindow, app } from 'electron';
import { download } from 'electron-dl';
import fs from 'fs';
import path from 'path';
import { spawn } from 'child_process';
import Log from 'electron-log';

const piperDir = path.join(app.getPath('userData'), 'piper');
const piperExe = path.join(piperDir, 'piper.exe');
const modelsDir = path.join(piperDir, 'models');

// GitHub release URLs for Piper Windows binary
const PIPER_BINARY_URL = 'https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_windows_amd64.zip';

const DEFAULT_MODEL_NAME = 'en_US-ryan-high';

export interface PiperVoice {
    id: string;
    name: string;
    language: string;
    gender: string;
    quality: string;
    sizeMB: number;
    onnxUrl: string;
    configUrl: string;
    isDownloaded?: boolean;
}

// Voices sourced from https://huggingface.co/rhasspy/piper-voices/tree/main
const HF_BASE = 'https://huggingface.co/rhasspy/piper-voices/resolve/main';

function voice(id: string, name: string, language: string, gender: string, quality: string, sizeMB: number, p: string): PiperVoice {
    return { id, name, language, gender, quality, sizeMB, onnxUrl: `${HF_BASE}/${p}/${id}.onnx`, configUrl: `${HF_BASE}/${p}/${id}.onnx.json` };
}

const PIPER_VOICES: PiperVoice[] = [
    // English (US)
    voice('en_US-lessac-medium',             'Lessac',                  'English (US)', 'Female', 'Medium', 63,  'en/en_US/lessac/medium'),
    voice('en_US-lessac-high',               'Lessac',                  'English (US)', 'Female', 'High',   117, 'en/en_US/lessac/high'),
    voice('en_US-ryan-medium',               'Ryan',                    'English (US)', 'Male',   'Medium', 63,  'en/en_US/ryan/medium'),
    voice('en_US-ryan-high',                 'Ryan',                    'English (US)', 'Male',   'High',   121, 'en/en_US/ryan/high'),
    voice('en_US-amy-medium',                'Amy',                     'English (US)', 'Female', 'Medium', 63,  'en/en_US/amy/medium'),
    voice('en_US-kristin-medium',            'Kristin',                 'English (US)', 'Female', 'Medium', 63,  'en/en_US/kristin/medium'),
    voice('en_US-hfc_female-medium',         'HFC Female',              'English (US)', 'Female', 'Medium', 63,  'en/en_US/hfc_female/medium'),
    voice('en_US-joe-medium',                'Joe',                     'English (US)', 'Male',   'Medium', 63,  'en/en_US/joe/medium'),
    voice('en_US-john-medium',               'John',                    'English (US)', 'Male',   'Medium', 63,  'en/en_US/john/medium'),
    voice('en_US-bryce-medium',              'Bryce',                   'English (US)', 'Male',   'Medium', 63,  'en/en_US/bryce/medium'),
    voice('en_US-kusal-medium',              'Kusal',                   'English (US)', 'Male',   'Medium', 63,  'en/en_US/kusal/medium'),
    voice('en_US-hfc_male-medium',           'HFC Male',                'English (US)', 'Male',   'Medium', 63,  'en/en_US/hfc_male/medium'),
    voice('en_US-libritts_r-medium',         'LibriTTS',                'English (US)', 'Mixed',  'Medium', 74,  'en/en_US/libritts_r/medium'),
    voice('en_US-kathleen-low',              'Kathleen',                'English (US)', 'Female', 'Low',    5,   'en/en_US/kathleen/low'),
    voice('en_US-danny-low',                 'Danny',                   'English (US)', 'Male',   'Low',    5,   'en/en_US/danny/low'),
    // English (GB)
    voice('en_GB-jenny_dioco-medium',        'Jenny',                   'English (GB)', 'Female', 'Medium', 63,  'en/en_GB/jenny_dioco/medium'),
    voice('en_GB-alba-medium',               'Alba',                    'English (GB)', 'Female', 'Medium', 63,  'en/en_GB/alba/medium'),
    voice('en_GB-cori-medium',               'Cori',                    'English (GB)', 'Female', 'Medium', 63,  'en/en_GB/cori/medium'),
    voice('en_GB-cori-high',                 'Cori',                    'English (GB)', 'Female', 'High',   117, 'en/en_GB/cori/high'),
    voice('en_GB-southern_english_female-low','Southern English Female', 'English (GB)', 'Female', 'Low',   5,   'en/en_GB/southern_english_female/low'),
    voice('en_GB-alan-medium',               'Alan',                    'English (GB)', 'Male',   'Medium', 63,  'en/en_GB/alan/medium'),
    voice('en_GB-northern_english_male-medium','Northern English Male',  'English (GB)', 'Male',   'Medium', 63,  'en/en_GB/northern_english_male/medium'),
    voice('en_GB-vctk-medium',               'VCTK',                    'English (GB)', 'Mixed',  'Medium', 110, 'en/en_GB/vctk/medium'),
    // German
    voice('de_DE-thorsten-medium',           'Thorsten',                'German (DE)',  'Male',   'Medium', 63,  'de/de_DE/thorsten/medium'),
    voice('de_DE-thorsten-high',             'Thorsten',                'German (DE)',  'Male',   'High',   117, 'de/de_DE/thorsten/high'),
    voice('de_DE-thorsten_emotional-medium', 'Thorsten (Emotional)',    'German (DE)',  'Male',   'Medium', 63,  'de/de_DE/thorsten_emotional/medium'),
    voice('de_DE-kerstin-low',               'Kerstin',                 'German (DE)',  'Female', 'Low',    5,   'de/de_DE/kerstin/low'),
    voice('de_DE-ramona-low',                'Ramona',                  'German (DE)',  'Female', 'Low',    5,   'de/de_DE/ramona/low'),
    voice('de_DE-eva_k-x_low',              'Eva',                     'German (DE)',  'Female', 'Low',    5,   'de/de_DE/eva_k/x_low'),
    voice('de_DE-karlsson-low',              'Karlsson',                'German (DE)',  'Male',   'Low',    5,   'de/de_DE/karlsson/low'),
    // Spanish (Spain)
    voice('es_ES-sharvard-medium',           'Sharvard',                'Spanish (ES)', 'Male',   'Medium', 77,  'es/es_ES/sharvard/medium'),
    voice('es_ES-mls_10246-low',             'MLS Female',              'Spanish (ES)', 'Female', 'Low',    8,   'es/es_ES/mls_10246/low'),
    voice('es_ES-mls_9972-low',              'MLS Male',                'Spanish (ES)', 'Male',   'Low',    8,   'es/es_ES/mls_9972/low'),
    voice('es_ES-carlfm-x_low',             'Carlfm',                  'Spanish (ES)', 'Male',   'Low',    5,   'es/es_ES/carlfm/x_low'),
    // Spanish (Mexico)
    voice('es_MX-ald-medium',                'Ald',                     'Spanish (MX)', 'Male',   'Medium', 63,  'es/es_MX/ald/medium'),
    voice('es_MX-claude-high',               'Claude',                  'Spanish (MX)', 'Male',   'High',   121, 'es/es_MX/claude/high'),
    // French
    voice('fr_FR-siwis-medium',              'Siwis',                   'French (FR)',  'Female', 'Medium', 63,  'fr/fr_FR/siwis/medium'),
    voice('fr_FR-siwis-low',                 'Siwis',                   'French (FR)',  'Female', 'Low',    5,   'fr/fr_FR/siwis/low'),
    // Italian
    voice('it_IT-paola-medium',              'Paola',                   'Italian (IT)', 'Female', 'Medium', 63,  'it/it_IT/paola/medium'),
    voice('it_IT-riccardo-x_low',            'Riccardo',                'Italian (IT)', 'Male',   'Low',    5,   'it/it_IT/riccardo/x_low'),
    // Portuguese (Brazil)
    voice('pt_BR-faber-medium',              'Faber',                   'Portuguese (BR)', 'Male', 'Medium', 63, 'pt/pt_BR/faber/medium'),
];

function ensureDir(dir: string) {
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function isModelDownloaded(modelId: string): boolean {
    return (
        fs.existsSync(path.join(modelsDir, `${modelId}.onnx`)) &&
        fs.existsSync(path.join(modelsDir, `${modelId}.onnx.json`))
    );
}

function getPiperStatus(): { binaryReady: boolean; modelReady: boolean; modelName: string } {
    const binaryReady = fs.existsSync(piperExe);
    const modelReady = isModelDownloaded(DEFAULT_MODEL_NAME);
    return { binaryReady, modelReady, modelName: DEFAULT_MODEL_NAME };
}

async function extractPiperZip(zipPath: string): Promise<boolean> {
    try {
        const extract = (await import('extract-zip')).default;
        const tmpDir = path.join(piperDir, '_tmp_extract');
        ensureDir(tmpDir);
        await extract(zipPath, { dir: tmpDir });

        // Piper zip contains a subdirectory (e.g. "piper/") with piper.exe, DLLs,
        // and espeak-ng-data/. Preserve directory structure so piper.exe can find
        // both DLLs and espeak-ng-data/ at runtime.
        function copyContents(srcDir: string, destDir: string) {
            ensureDir(destDir);
            for (const f of fs.readdirSync(srcDir)) {
                const full = path.join(srcDir, f);
                const dest = path.join(destDir, f);
                if (fs.statSync(full).isDirectory()) {
                    copyContents(full, dest);
                } else {
                    fs.copyFileSync(full, dest);
                    Log.info('[Piper] Extracted:', f);
                }
            }
        }

        // Find the inner piper/ subdirectory (the zip has one top-level folder)
        const entries = fs.readdirSync(tmpDir);
        const innerDir =
            entries.length === 1 && fs.statSync(path.join(tmpDir, entries[0])).isDirectory()
                ? path.join(tmpDir, entries[0])
                : tmpDir;
        copyContents(innerDir, piperDir);

        if (!fs.existsSync(piperExe)) throw new Error('piper.exe not found after extraction');

        fs.rmSync(tmpDir, { recursive: true, force: true });
        fs.unlinkSync(zipPath);
        Log.info('[Piper] Binary and DLLs extracted to', piperDir);
        return true;
    } catch (err) {
        Log.error('[Piper] Extract failed:', err);
        return false;
    }
}

export function PiperTTSHandlers(mainWindow: BrowserWindow) {

    // Check if piper binary + default model are ready
    ipcMain.handle('piper:status', () => getPiperStatus());

    // Return all available voices with download status
    ipcMain.handle('piper:voices', () =>
        PIPER_VOICES.map(v => ({ ...v, isDownloaded: isModelDownloaded(v.id) }))
    );

    // Download binary + default model, reporting progress
    ipcMain.handle('piper:install', async () => {
        ensureDir(piperDir);
        ensureDir(modelsDir);

        try {
            // Step 1: Download piper binary zip (~4MB)
            mainWindow.webContents.send('piper:install-progress', { step: 'binary', percent: 0 });
            const zipPath = path.join(piperDir, 'piper.zip');

            await download(mainWindow, PIPER_BINARY_URL, {
                directory: piperDir,
                filename: 'piper.zip',
                saveAs: false,
                overwrite: true,
                onProgress: (p) => {
                    mainWindow.webContents.send('piper:install-progress', {
                        step: 'binary',
                        percent: Math.floor(p.percent * 100),
                    });
                },
            });

            const extracted = await extractPiperZip(zipPath);
            if (!extracted) return { success: false, error: 'Failed to extract piper binary' };

            // Step 2: Download default model .onnx (~63MB)
            mainWindow.webContents.send('piper:install-progress', { step: 'model', percent: 0 });
            const defaultVoice = PIPER_VOICES.find(v => v.id === DEFAULT_MODEL_NAME)!;
            await download(mainWindow, defaultVoice.onnxUrl, {
                directory: modelsDir,
                filename: `${DEFAULT_MODEL_NAME}.onnx`,
                saveAs: false,
                overwrite: true,
                onProgress: (p) => {
                    mainWindow.webContents.send('piper:install-progress', {
                        step: 'model',
                        percent: Math.floor(p.percent * 100),
                    });
                },
            });

            // Step 3: Download model config (~5KB)
            mainWindow.webContents.send('piper:install-progress', { step: 'config', percent: 0 });
            await download(mainWindow, defaultVoice.configUrl, {
                directory: modelsDir,
                filename: `${DEFAULT_MODEL_NAME}.onnx.json`,
                saveAs: false,
                overwrite: true,
            });

            mainWindow.webContents.send('piper:install-progress', { step: 'done', percent: 100 });
            return { success: true, modelName: DEFAULT_MODEL_NAME };
        } catch (err: any) {
            Log.error('[Piper] Install failed:', err);
            return { success: false, error: err?.message ?? 'Unknown error' };
        }
    });

    // Download an additional voice model
    ipcMain.handle('piper:installModel', async (_, voiceId: string) => {
        const voice = PIPER_VOICES.find(v => v.id === voiceId);
        if (!voice) return { success: false, error: 'Unknown voice' };

        ensureDir(modelsDir);

        try {
            await download(mainWindow, voice.onnxUrl, {
                directory: modelsDir,
                filename: `${voiceId}.onnx`,
                saveAs: false,
                overwrite: true,
                onProgress: (p) => {
                    mainWindow.webContents.send('piper:model-progress', {
                        voiceId,
                        percent: Math.floor(p.percent * 100),
                    });
                },
            });

            await download(mainWindow, voice.configUrl, {
                directory: modelsDir,
                filename: `${voiceId}.onnx.json`,
                saveAs: false,
                overwrite: true,
            });

            Log.info('[Piper] Voice installed:', voiceId);
            return { success: true };
        } catch (err: any) {
            Log.error('[Piper] Voice install failed:', voiceId, err);
            return { success: false, error: err?.message ?? 'Unknown error' };
        }
    });

    // Delete a voice model
    ipcMain.handle('piper:deleteModel', (_, voiceId: string): { success: boolean; error?: string } => {
        try {
            const onnx = path.join(modelsDir, `${voiceId}.onnx`);
            const config = path.join(modelsDir, `${voiceId}.onnx.json`);
            if (fs.existsSync(onnx)) fs.unlinkSync(onnx);
            if (fs.existsSync(config)) fs.unlinkSync(config);
            Log.info('[Piper] Voice deleted:', voiceId);
            return { success: true };
        } catch (err: any) {
            Log.error('[Piper] Voice delete failed:', voiceId, err);
            return { success: false, error: err?.message ?? 'Unknown error' };
        }
    });

    // Uninstall — remove the entire piper directory
    ipcMain.handle('piper:uninstall', (): { success: boolean; error?: string } => {
        try {
            if (fs.existsSync(piperDir)) {
                fs.rmSync(piperDir, { recursive: true, force: true });
                Log.info('[Piper] Uninstalled — removed', piperDir);
            }
            return { success: true };
        } catch (err: any) {
            Log.error('[Piper] Uninstall failed:', err);
            return { success: false, error: err?.message ?? 'Unknown error' };
        }
    });

    // Speak text using piper, return WAV as base64
    ipcMain.handle('piper:speak', async (_event, text: string, modelId?: string): Promise<{ success: boolean; wav?: string; error?: string }> => {
        const voiceId = modelId ?? DEFAULT_MODEL_NAME;
        const binaryReady = fs.existsSync(piperExe);
        if (!binaryReady || !isModelDownloaded(voiceId)) {
            // Fall back to default if requested model not found
            if (voiceId !== DEFAULT_MODEL_NAME && isModelDownloaded(DEFAULT_MODEL_NAME)) {
                return handleSpeak(text, DEFAULT_MODEL_NAME);
            }
            return { success: false, error: 'Piper not installed' };
        }

        return handleSpeak(text, voiceId);
    });
}

function handleSpeak(text: string, voiceId: string): Promise<{ success: boolean; wav?: string; error?: string }> {
    const modelFile = path.join(modelsDir, `${voiceId}.onnx`);
    const espeakData = path.join(piperDir, 'espeak-ng-data');

    return new Promise((resolve) => {
        const chunks: Buffer[] = [];

        const proc = spawn(piperExe, [
            '--model', modelFile,
            '--output_raw',
            '--espeak_data', espeakData,
        ]);

        proc.stdout.on('data', (chunk: Buffer) => chunks.push(chunk));

        proc.stderr.on('data', (data: Buffer) => {
            Log.info('[Piper stderr]', data.toString());
        });

        proc.on('close', (code) => {
            if (code !== 0 && chunks.length === 0) {
                resolve({ success: false, error: `Piper exited with code ${code}` });
                return;
            }
            const raw = Buffer.concat(chunks);
            // Wrap raw PCM (22050Hz, 16-bit mono) in a WAV header
            const wav = buildWav(raw, 22050, 1, 16);
            resolve({ success: true, wav: wav.toString('base64') });
        });

        proc.on('error', (err) => {
            Log.error('[Piper] spawn error:', err);
            resolve({ success: false, error: err.message });
        });

        proc.stdin.write(text);
        proc.stdin.end();
    });
}

// Build a minimal WAV header around raw PCM data
function buildWav(pcm: Buffer, sampleRate: number, channels: number, bitDepth: number): Buffer {
    const byteRate = (sampleRate * channels * bitDepth) / 8;
    const blockAlign = (channels * bitDepth) / 8;
    const header = Buffer.alloc(44);

    header.write('RIFF', 0);
    header.writeUInt32LE(36 + pcm.length, 4);
    header.write('WAVE', 8);
    header.write('fmt ', 12);
    header.writeUInt32LE(16, 16);          // PCM chunk size
    header.writeUInt16LE(1, 20);           // PCM format
    header.writeUInt16LE(channels, 22);
    header.writeUInt32LE(sampleRate, 24);
    header.writeUInt32LE(byteRate, 28);
    header.writeUInt16LE(blockAlign, 32);
    header.writeUInt16LE(bitDepth, 34);
    header.write('data', 36);
    header.writeUInt32LE(pcm.length, 40);

    return Buffer.concat([header, pcm]);
}
