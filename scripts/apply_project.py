from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path('/home/ubuntu/routine-tracker')

def write(rel: str, content: str):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.lstrip('\n'), encoding='utf-8')

write('package.json', r'''
{
  "name": "routine-tracker",
  "private": true,
  "version": "1.0.0",
  "description": "Purple cinematic macOS routine and habit tracker",
  "author": "Manus",
  "type": "module",
  "main": "dist-main/main.cjs",
  "scripts": {
    "dev": "concurrently -k \"vite --host 127.0.0.1\" \"wait-on http://127.0.0.1:5173 && pnpm build:main && electron .\"",
    "build:main": "esbuild src/main/main.ts src/main/preload.ts --bundle --platform=node --format=cjs --outdir=dist-main --out-extension:.js=.cjs --external:electron --external:better-sqlite3",
    "build": "tsc -b && vite build && pnpm build:main",
    "pack:mac": "pnpm build && electron-builder --mac dmg --x64 --arm64",
    "pack:linux": "pnpm build && electron-builder --linux AppImage --x64",
    "preview": "vite preview"
  },
  "dependencies": {
    "@vitejs/plugin-react": "latest",
    "better-sqlite3": "^12.9.0",
    "canvas-confetti": "^1.9.4",
    "electron": "^28.3.3",
    "framer-motion": "^12.23.26",
    "howler": "^2.2.4",
    "lucide-react": "^0.555.0",
    "react": "^19.2.0",
    "react-dom": "^19.2.0",
    "recharts": "^3.5.1"
  },
  "devDependencies": {
    "@types/better-sqlite3": "^7.6.13",
    "@types/canvas-confetti": "^1.9.0",
    "@types/howler": "^2.2.12",
    "@types/node": "latest",
    "@types/react": "latest",
    "@types/react-dom": "latest",
    "concurrently": "^9.2.1",
    "electron-builder": "^26.8.1",
    "esbuild": "^0.28.0",
    "typescript": "~5.9.3",
    "vite": "^8.0.11",
    "wait-on": "^9.0.5"
  },
  "build": {
    "appId": "im.manus.routinetracker",
    "productName": "Routine Tracker",
    "copyright": "Copyright © 2026",
    "directories": {
      "output": "dist-release",
      "buildResources": "build"
    },
    "files": [
      "dist/**",
      "dist-main/**",
      "package.json"
    ],
    "asarUnpack": [
      "node_modules/better-sqlite3/**"
    ],
    "npmRebuild": true,
    "mac": {
      "category": "public.app-category.productivity",
      "target": [
        {
          "target": "dmg",
          "arch": ["x64", "arm64"]
        }
      ],
      "icon": "build/icon.icns",
      "hardenedRuntime": false,
      "gatekeeperAssess": false
    },
    "dmg": {
      "background": "build/dmg-background.png",
      "iconSize": 128,
      "window": {
        "width": 560,
        "height": 360
      },
      "contents": [
        { "x": 160, "y": 180, "type": "file" },
        { "x": 400, "y": 180, "type": "link", "path": "/Applications" }
      ]
    },
    "linux": {
      "target": "AppImage",
      "icon": "build/icon.png",
      "category": "Utility"
    }
  }
}
''')

write('index.html', r'''
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="theme-color" content="#7C3AED" />
    <title>Routine Tracker</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/renderer/main.tsx"></script>
  </body>
</html>
''')

write('tsconfig.json', r'''
{
  "files": [],
  "references": [
    { "path": "./tsconfig.app.json" },
    { "path": "./tsconfig.node.json" }
  ]
}
''')

write('tsconfig.app.json', r'''
{
  "compilerOptions": {
    "tsBuildInfoFile": "./node_modules/.tmp/tsconfig.app.tsbuildinfo",
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "allowJs": false,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "noUnusedLocals": false,
    "noUnusedParameters": false,
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx"
  },
  "include": ["src/renderer", "src/shared"]
}
''')

write('tsconfig.node.json', r'''
{
  "compilerOptions": {
    "tsBuildInfoFile": "./node_modules/.tmp/tsconfig.node.tsbuildinfo",
    "target": "ES2020",
    "lib": ["ES2020"],
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "allowSyntheticDefaultImports": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "strict": true,
    "noUnusedLocals": false,
    "noUnusedParameters": false,
    "noEmit": true,
    "types": ["node"]
  },
  "include": ["vite.config.ts", "src/main", "src/shared"]
}
''')

write('vite.config.ts', r'''
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  root: '.',
  base: './',
  build: {
    outDir: 'dist',
    emptyOutDir: true
  },
  server: {
    port: 5173,
    strictPort: true
  }
});
''')

write('src/shared/types.ts', r'''
export type ViewKey = 'daily' | 'weekly' | 'monthly' | 'analytics' | 'settings';
export type ThemeMode = 'light' | 'dark' | 'system';
export type EffectIntensity = 'subtle' | 'normal' | 'cinematic';

export interface Task {
  id: number;
  date: string;
  title: string;
  completed: number;
  category?: string | null;
  notes?: string | null;
  created_at: string;
}

export interface Habit {
  id: number;
  name: string;
  goal_per_month: number;
  color: string;
  streak_count: number;
  created_at: string;
}

export interface HabitRecord {
  id: number;
  habit_id: number;
  date: string;
  completed: number;
}

export interface DayNote {
  id: number;
  date: string;
  content: string;
}

export interface Achievement {
  id: number;
  type: string;
  title: string;
  unlocked_at: string;
}

export interface SettingsState {
  theme: ThemeMode;
  sound: boolean;
  effectIntensity: EffectIntensity;
  cinematicMode: boolean;
}

export interface AppState {
  tasks: Task[];
  habits: Habit[];
  habitRecords: HabitRecord[];
  notes: DayNote[];
  achievements: Achievement[];
  settings: SettingsState;
}

export interface RoutineAPI {
  getState: () => Promise<AppState>;
  addTask: (input: { date: string; title: string; category?: string }) => Promise<Task>;
  updateTask: (task: Partial<Task> & { id: number }) => Promise<Task>;
  deleteTask: (id: number) => Promise<{ ok: boolean }>;
  setNote: (input: { date: string; content: string }) => Promise<DayNote>;
  addHabit: (input: { name: string; goal_per_month?: number; color?: string }) => Promise<Habit>;
  toggleHabitRecord: (input: { habit_id: number; date: string }) => Promise<HabitRecord>;
  updateSettings: (settings: Partial<SettingsState>) => Promise<SettingsState>;
  exportData: () => Promise<AppState>;
  importData: (payload: AppState) => Promise<{ ok: boolean }>;
  notifyDemo: () => Promise<{ ok: boolean }>;
}
''')

write('src/main/preload.ts', r'''
import { contextBridge, ipcRenderer } from 'electron';
import type { AppState, SettingsState } from '../shared/types';

contextBridge.exposeInMainWorld('routineAPI', {
  getState: () => ipcRenderer.invoke('app:get-state'),
  addTask: (input: { date: string; title: string; category?: string }) => ipcRenderer.invoke('task:add', input),
  updateTask: (task: { id: number; title?: string; completed?: number; category?: string; notes?: string }) => ipcRenderer.invoke('task:update', task),
  deleteTask: (id: number) => ipcRenderer.invoke('task:delete', id),
  setNote: (input: { date: string; content: string }) => ipcRenderer.invoke('note:set', input),
  addHabit: (input: { name: string; goal_per_month?: number; color?: string }) => ipcRenderer.invoke('habit:add', input),
  toggleHabitRecord: (input: { habit_id: number; date: string }) => ipcRenderer.invoke('habit:toggle-record', input),
  updateSettings: (settings: Partial<SettingsState>) => ipcRenderer.invoke('settings:update', settings),
  exportData: (): Promise<AppState> => ipcRenderer.invoke('data:export'),
  importData: (payload: AppState) => ipcRenderer.invoke('data:import', payload),
  notifyDemo: () => ipcRenderer.invoke('notify:demo')
});
''')

write('src/main/main.ts', r'''
import { app, BrowserWindow, ipcMain, Menu, Notification, nativeTheme, shell } from 'electron';
import path from 'node:path';
import fs from 'node:fs';
import Database from 'better-sqlite3';
import type { AppState, SettingsState, Task, Habit, HabitRecord, DayNote } from '../shared/types';

const isDev = !app.isPackaged;
let mainWindow: BrowserWindow | null = null;
let db: Database.Database;
let settings: SettingsState = { theme: 'system', sound: true, effectIntensity: 'normal', cinematicMode: true };

const todayISO = (offset = 0) => {
  const date = new Date();
  date.setDate(date.getDate() + offset);
  return date.toISOString().slice(0, 10);
};

const nowISO = () => new Date().toISOString();

function getUserDataPath(file: string) {
  return path.join(app.getPath('userData'), file);
}

function loadSettings() {
  const file = getUserDataPath('settings.json');
  if (fs.existsSync(file)) {
    settings = { ...settings, ...JSON.parse(fs.readFileSync(file, 'utf-8')) };
  }
  nativeTheme.themeSource = settings.theme;
}

function saveSettings() {
  fs.writeFileSync(getUserDataPath('settings.json'), JSON.stringify(settings, null, 2));
  nativeTheme.themeSource = settings.theme;
}

function initDatabase() {
  const dbPath = getUserDataPath('routine-tracker.sqlite');
  db = new Database(dbPath);
  db.pragma('journal_mode = WAL');
  db.exec(`
    CREATE TABLE IF NOT EXISTS tasks (
      id INTEGER PRIMARY KEY,
      date TEXT NOT NULL,
      title TEXT NOT NULL,
      completed INTEGER DEFAULT 0,
      category TEXT,
      notes TEXT,
      created_at TEXT
    );
    CREATE TABLE IF NOT EXISTS habits (
      id INTEGER PRIMARY KEY,
      name TEXT NOT NULL,
      goal_per_month INTEGER DEFAULT 30,
      color TEXT DEFAULT '#7C3AED',
      streak_count INTEGER DEFAULT 0,
      created_at TEXT
    );
    CREATE TABLE IF NOT EXISTS habit_records (
      id INTEGER PRIMARY KEY,
      habit_id INTEGER,
      date TEXT NOT NULL,
      completed INTEGER DEFAULT 0,
      FOREIGN KEY (habit_id) REFERENCES habits(id),
      UNIQUE(habit_id, date)
    );
    CREATE TABLE IF NOT EXISTS notes (
      id INTEGER PRIMARY KEY,
      date TEXT NOT NULL UNIQUE,
      content TEXT
    );
    CREATE TABLE IF NOT EXISTS achievements (
      id INTEGER PRIMARY KEY,
      type TEXT,
      title TEXT,
      unlocked_at TEXT
    );
  `);
  seedDataIfEmpty();
}

function seedDataIfEmpty() {
  const taskCount = db.prepare('SELECT COUNT(*) as count FROM tasks').get() as { count: number };
  if (taskCount.count > 0) return;

  const taskInsert = db.prepare('INSERT INTO tasks (date, title, completed, category, notes, created_at) VALUES (?, ?, ?, ?, ?, ?)');
  const samples = [
    ['Deep work sprint 90 minutes', 1, 'Focus'],
    ['Morning stretch and water', 1, 'Health'],
    ['Draft creative concept', 0, 'Creation'],
    ['Inbox zero ritual', 0, 'Admin'],
    ['Read 15 pages', 0, 'Growth'],
    ['Plan tomorrow setup', 0, 'Planning']
  ];
  for (const [title, completed, category] of samples) taskInsert.run(todayISO(), title, completed, category, '', nowISO());
  for (let offset = -3; offset <= 6; offset++) {
    if (offset === 0) continue;
    taskInsert.run(todayISO(offset), 'Capture one useful idea', Math.random() > 0.35 ? 1 : 0, 'Creation', '', nowISO());
    taskInsert.run(todayISO(offset), 'Move body for 20 minutes', Math.random() > 0.45 ? 1 : 0, 'Health', '', nowISO());
    taskInsert.run(todayISO(offset), 'No-scroll focus block', Math.random() > 0.5 ? 1 : 0, 'Focus', '', nowISO());
  }

  const habitInsert = db.prepare('INSERT INTO habits (name, goal_per_month, color, streak_count, created_at) VALUES (?, ?, ?, ?, ?)');
  const habitIds = [
    habitInsert.run('Creative Deep Work', 24, '#7C3AED', 7, nowISO()).lastInsertRowid,
    habitInsert.run('Workout', 20, '#A78BFA', 4, nowISO()).lastInsertRowid,
    habitInsert.run('Reading', 26, '#C4B5FD', 12, nowISO()).lastInsertRowid,
    habitInsert.run('No Sugar', 18, '#8B5CF6', 3, nowISO()).lastInsertRowid,
    habitInsert.run('Evening Review', 22, '#DDD6FE', 8, nowISO()).lastInsertRowid
  ];
  const recordInsert = db.prepare('INSERT OR IGNORE INTO habit_records (habit_id, date, completed) VALUES (?, ?, ?)');
  const current = new Date();
  const year = current.getFullYear();
  const month = current.getMonth();
  const days = new Date(year, month + 1, 0).getDate();
  for (const habitId of habitIds) {
    for (let d = 1; d <= days; d++) {
      const iso = new Date(year, month, d).toISOString().slice(0, 10);
      const chance = d <= current.getDate() ? 0.66 + (Number(habitId) % 3) * 0.06 : 0.06;
      recordInsert.run(habitId, iso, Math.random() < chance ? 1 : 0);
    }
  }
  db.prepare('INSERT INTO notes (date, content) VALUES (?, ?)').run(todayISO(), '오늘은 촬영용 데모 데이터를 포함해 바로 후킹 컷을 만들 수 있도록 세팅되었습니다. 체크박스를 눌러 보라 파티클, 글로우, 도넛 카운트업을 확인하세요.');
}

function getState(): AppState {
  const tasks = db.prepare('SELECT * FROM tasks ORDER BY date ASC, id ASC').all() as Task[];
  const habits = db.prepare('SELECT * FROM habits ORDER BY id ASC').all() as Habit[];
  const habitRecords = db.prepare('SELECT * FROM habit_records ORDER BY date ASC, habit_id ASC').all() as HabitRecord[];
  const notes = db.prepare('SELECT * FROM notes ORDER BY date ASC').all() as DayNote[];
  const achievements = db.prepare('SELECT * FROM achievements ORDER BY unlocked_at DESC').all() as AppState['achievements'];
  return { tasks, habits, habitRecords, notes, achievements, settings };
}

function registerIpc() {
  ipcMain.handle('app:get-state', () => getState());
  ipcMain.handle('task:add', (_event, input: { date: string; title: string; category?: string }) => {
    const result = db.prepare('INSERT INTO tasks (date, title, completed, category, notes, created_at) VALUES (?, ?, 0, ?, ?, ?)')
      .run(input.date, input.title, input.category ?? 'Focus', '', nowISO());
    return db.prepare('SELECT * FROM tasks WHERE id = ?').get(result.lastInsertRowid) as Task;
  });
  ipcMain.handle('task:update', (_event, task: Partial<Task> & { id: number }) => {
    const existing = db.prepare('SELECT * FROM tasks WHERE id = ?').get(task.id) as Task;
    const next = { ...existing, ...task };
    db.prepare('UPDATE tasks SET title = ?, completed = ?, category = ?, notes = ? WHERE id = ?')
      .run(next.title, next.completed ? 1 : 0, next.category ?? null, next.notes ?? null, next.id);
    return db.prepare('SELECT * FROM tasks WHERE id = ?').get(task.id) as Task;
  });
  ipcMain.handle('task:delete', (_event, id: number) => {
    db.prepare('DELETE FROM tasks WHERE id = ?').run(id);
    return { ok: true };
  });
  ipcMain.handle('note:set', (_event, input: { date: string; content: string }) => {
    db.prepare('INSERT INTO notes (date, content) VALUES (?, ?) ON CONFLICT(date) DO UPDATE SET content = excluded.content')
      .run(input.date, input.content);
    return db.prepare('SELECT * FROM notes WHERE date = ?').get(input.date) as DayNote;
  });
  ipcMain.handle('habit:add', (_event, input: { name: string; goal_per_month?: number; color?: string }) => {
    const result = db.prepare('INSERT INTO habits (name, goal_per_month, color, streak_count, created_at) VALUES (?, ?, ?, 0, ?)')
      .run(input.name, input.goal_per_month ?? 30, input.color ?? '#7C3AED', nowISO());
    return db.prepare('SELECT * FROM habits WHERE id = ?').get(result.lastInsertRowid) as Habit;
  });
  ipcMain.handle('habit:toggle-record', (_event, input: { habit_id: number; date: string }) => {
    const existing = db.prepare('SELECT * FROM habit_records WHERE habit_id = ? AND date = ?').get(input.habit_id, input.date) as HabitRecord | undefined;
    if (existing) {
      db.prepare('UPDATE habit_records SET completed = ? WHERE id = ?').run(existing.completed ? 0 : 1, existing.id);
      return db.prepare('SELECT * FROM habit_records WHERE id = ?').get(existing.id) as HabitRecord;
    }
    const result = db.prepare('INSERT INTO habit_records (habit_id, date, completed) VALUES (?, ?, 1)').run(input.habit_id, input.date);
    return db.prepare('SELECT * FROM habit_records WHERE id = ?').get(result.lastInsertRowid) as HabitRecord;
  });
  ipcMain.handle('settings:update', (_event, nextSettings: Partial<SettingsState>) => {
    settings = { ...settings, ...nextSettings };
    saveSettings();
    return settings;
  });
  ipcMain.handle('data:export', () => getState());
  ipcMain.handle('data:import', (_event, payload: AppState) => {
    const tx = db.transaction(() => {
      db.exec('DELETE FROM habit_records; DELETE FROM tasks; DELETE FROM habits; DELETE FROM notes; DELETE FROM achievements;');
      const taskInsert = db.prepare('INSERT INTO tasks (id, date, title, completed, category, notes, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)');
      payload.tasks.forEach(t => taskInsert.run(t.id, t.date, t.title, t.completed, t.category, t.notes, t.created_at));
      const habitInsert = db.prepare('INSERT INTO habits (id, name, goal_per_month, color, streak_count, created_at) VALUES (?, ?, ?, ?, ?, ?)');
      payload.habits.forEach(h => habitInsert.run(h.id, h.name, h.goal_per_month, h.color, h.streak_count, h.created_at));
      const recordInsert = db.prepare('INSERT INTO habit_records (id, habit_id, date, completed) VALUES (?, ?, ?, ?)');
      payload.habitRecords.forEach(r => recordInsert.run(r.id, r.habit_id, r.date, r.completed));
      const noteInsert = db.prepare('INSERT INTO notes (id, date, content) VALUES (?, ?, ?)');
      payload.notes.forEach(n => noteInsert.run(n.id, n.date, n.content));
    });
    tx();
    settings = { ...settings, ...payload.settings };
    saveSettings();
    return { ok: true };
  });
  ipcMain.handle('notify:demo', () => {
    if (Notification.isSupported()) {
      new Notification({ title: 'Routine Tracker', body: '오늘의 루틴 시작! 보라색 몰입 모드가 준비되었습니다.' }).show();
    }
    return { ok: true };
  });
}

function buildMenu() {
  const template: Electron.MenuItemConstructorOptions[] = [
    {
      label: 'Routine Tracker',
      submenu: [
        { role: 'about' },
        { type: 'separator' },
        { label: 'Open User Data', click: () => shell.openPath(app.getPath('userData')) },
        { type: 'separator' },
        { role: 'quit' }
      ]
    },
    {
      label: 'File',
      submenu: [
        { label: 'New Task', accelerator: 'CommandOrControl+N', click: () => mainWindow?.webContents.send('shortcut:new-task') },
        { type: 'separator' },
        { role: 'close' }
      ]
    },
    { label: 'Edit', submenu: [{ role: 'undo' }, { role: 'redo' }, { type: 'separator' }, { role: 'cut' }, { role: 'copy' }, { role: 'paste' }] },
    {
      label: 'View',
      submenu: [
        { label: 'Daily', accelerator: 'CommandOrControl+1', click: () => mainWindow?.webContents.send('shortcut:view', 'daily') },
        { label: 'Weekly', accelerator: 'CommandOrControl+2', click: () => mainWindow?.webContents.send('shortcut:view', 'weekly') },
        { label: 'Monthly', accelerator: 'CommandOrControl+3', click: () => mainWindow?.webContents.send('shortcut:view', 'monthly') },
        { label: 'Analytics', accelerator: 'CommandOrControl+4', click: () => mainWindow?.webContents.send('shortcut:view', 'analytics') },
        { type: 'separator' },
        { role: 'togglefullscreen' },
        { role: 'reload' }
      ]
    }
  ];
  Menu.setApplicationMenu(Menu.buildFromTemplate(template));
}

async function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1320,
    height: 860,
    minWidth: 1120,
    minHeight: 720,
    backgroundColor: '#0F0A1E',
    titleBarStyle: 'hiddenInset',
    vibrancy: process.platform === 'darwin' ? 'under-window' : undefined,
    visualEffectState: 'active',
    webPreferences: {
      preload: path.join(__dirname, 'preload.cjs'),
      contextIsolation: true,
      nodeIntegration: false
    }
  });

  if (isDev) {
    await mainWindow.loadURL('http://127.0.0.1:5173');
  } else {
    await mainWindow.loadFile(path.join(__dirname, '../dist/index.html'));
  }
}

app.whenReady().then(() => {
  loadSettings();
  initDatabase();
  registerIpc();
  buildMenu();
  createWindow();
  app.setAppUserModelId('im.manus.routinetracker');
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
''')

write('src/renderer/vite-env.d.ts', r'''
/// <reference types="vite/client" />
import type { RoutineAPI } from '../shared/types';

declare global {
  interface Window {
    routineAPI?: RoutineAPI;
  }
}
''')

write('src/renderer/effects/sound.ts', r'''
import { Howl } from 'howler';
import type { SettingsState } from '../../shared/types';

let masterVolume = 0.4;
let enabled = true;

const synth = (type: OscillatorType, frequencies: number[], duration = 0.25) => {
  if (!enabled) return;
  const AudioContextCtor = window.AudioContext || (window as unknown as { webkitAudioContext?: typeof AudioContext }).webkitAudioContext;
  if (!AudioContextCtor) return;
  const ctx = new AudioContextCtor();
  const gain = ctx.createGain();
  gain.gain.setValueAtTime(masterVolume * 0.18, ctx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + duration);
  gain.connect(ctx.destination);
  frequencies.forEach((frequency, index) => {
    const oscillator = ctx.createOscillator();
    oscillator.type = type;
    oscillator.frequency.setValueAtTime(frequency, ctx.currentTime + index * 0.025);
    oscillator.connect(gain);
    oscillator.start(ctx.currentTime + index * 0.025);
    oscillator.stop(ctx.currentTime + duration);
  });
};

const howl = (src: string) => new Howl({ src: [src], volume: masterVolume, preload: false, html5: false });

export const sound = {
  configure(settings: SettingsState) {
    enabled = settings.sound;
    masterVolume = settings.cinematicMode ? 0.46 : 0.4;
  },
  check() { synth('sine', [880, 1320], 0.32); },
  add() { synth('triangle', [1046, 1568], 0.2); },
  delete() { synth('sawtooth', [440], 0.16); },
  transition() { synth('sine', [330, 550], 0.25); },
  perfect() { synth('triangle', [523, 659, 784, 1046], 0.75); },
  hover() { synth('square', [660], 0.05); },
  sparkle() { synth('sine', [1175, 1760, 2349], 0.45); },
  customHowl(src: string) { return howl(src); }
};
''')

write('src/renderer/main.tsx', r'''
import React, { useEffect, useMemo, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { AnimatePresence, motion } from 'framer-motion';
import confetti from 'canvas-confetti';
import {
  BarChart, Bar, CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis
} from 'recharts';
import {
  Activity, CalendarDays, Check, ChevronRight, CirclePlus, Download, Flame, LayoutDashboard,
  Moon, Music2, Settings, Sparkles, Sun, Trash2, Trophy, Upload, Wand2
} from 'lucide-react';
import type { AppState, EffectIntensity, Habit, HabitRecord, SettingsState, Task, ViewKey } from '../shared/types';
import { sound } from './effects/sound';
import './styles.css';

const iso = (date = new Date()) => date.toISOString().slice(0, 10);
const pretty = (value: string) => new Date(`${value}T12:00:00`).toLocaleDateString('en-US', { weekday: 'long', month: '2-digit', day: '2-digit', year: 'numeric' });
const dayLabel = (value: string) => new Date(`${value}T12:00:00`).toLocaleDateString('en-US', { weekday: 'short' });
const monthKey = (value: string) => value.slice(0, 7);

const fallbackState = (): AppState => {
  const today = iso();
  const tasks: Task[] = ['Deep work sprint 90 minutes', 'Morning stretch and water', 'Draft creative concept', 'Inbox zero ritual', 'Read 15 pages'].map((title, index) => ({
    id: index + 1, date: today, title, completed: index < 2 ? 1 : 0, category: ['Focus', 'Health', 'Creation', 'Admin', 'Growth'][index], notes: '', created_at: new Date().toISOString()
  }));
  const habits: Habit[] = ['Creative Deep Work', 'Workout', 'Reading', 'No Sugar', 'Evening Review'].map((name, index) => ({
    id: index + 1, name, goal_per_month: 22 + index, color: ['#7C3AED', '#A78BFA', '#C4B5FD', '#8B5CF6', '#DDD6FE'][index], streak_count: 3 + index, created_at: new Date().toISOString()
  }));
  const records: HabitRecord[] = [];
  const now = new Date();
  const days = new Date(now.getFullYear(), now.getMonth() + 1, 0).getDate();
  habits.forEach((habit) => {
    for (let d = 1; d <= days; d += 1) {
      records.push({ id: habit.id * 100 + d, habit_id: habit.id, date: new Date(now.getFullYear(), now.getMonth(), d).toISOString().slice(0, 10), completed: d <= now.getDate() && (d + habit.id) % 3 !== 0 ? 1 : 0 });
    }
  });
  return { tasks, habits, habitRecords: records, notes: [{ id: 1, date: today, content: '브라우저 미리보기용 샘플 데이터입니다.' }], achievements: [], settings: { theme: 'system', sound: true, effectIntensity: 'cinematic', cinematicMode: true } };
};

function useRoutineState() {
  const [state, setState] = useState<AppState>(fallbackState());
  const reload = async () => {
    if (window.routineAPI) setState(await window.routineAPI.getState());
  };
  useEffect(() => { void reload(); }, []);
  return { state, setState, reload };
}

const ProgressDonut = ({ value, size = 190, label = 'Complete' }: { value: number; size?: number; label?: string }) => {
  const radius = (size - 24) / 2;
  const circumference = 2 * Math.PI * radius;
  const dash = circumference - (value / 100) * circumference;
  return (
    <motion.div className="donut-wrap" whileHover={{ scale: 1.025 }} transition={{ type: 'spring', stiffness: 170, damping: 14 }}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        <defs>
          <linearGradient id="donutGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#7C3AED" />
            <stop offset="55%" stopColor="#A78BFA" />
            <stop offset="100%" stopColor="#C4B5FD" />
          </linearGradient>
          <filter id="violetGlow"><feGaussianBlur stdDeviation="3.5" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
        </defs>
        <circle cx={size / 2} cy={size / 2} r={radius} stroke="rgba(124,58,237,.12)" strokeWidth="16" fill="transparent" />
        <motion.circle
          cx={size / 2} cy={size / 2} r={radius} stroke="url(#donutGradient)" strokeWidth="16" strokeLinecap="round" fill="transparent"
          strokeDasharray={circumference} initial={{ strokeDashoffset: circumference }} animate={{ strokeDashoffset: dash }} transition={{ duration: 0.85, ease: 'easeOut' }}
          transform={`rotate(-90 ${size / 2} ${size / 2})`} filter="url(#violetGlow)"
        />
      </svg>
      <div className="donut-center"><motion.strong key={Math.round(value)} initial={{ y: 12, opacity: 0 }} animate={{ y: 0, opacity: 1 }}>{Math.round(value)}%</motion.strong><span>{label}</span></div>
      {value === 100 && <div className="rotating-aura" />}
    </motion.div>
  );
};

const ParticleBurst = ({ fireKey }: { fireKey: number }) => {
  const particles = useMemo(() => Array.from({ length: 16 }, (_, index) => ({
    id: `${fireKey}-${index}`, angle: (Math.PI * 2 * index) / 16, distance: 58 + Math.random() * 44, size: 4 + Math.random() * 5, color: ['#7C3AED', '#A78BFA', '#C4B5FD'][index % 3]
  })), [fireKey]);
  if (!fireKey) return null;
  return <>{particles.map((p) => <motion.span key={p.id} className="particle" style={{ width: p.size, height: p.size, background: p.color }} initial={{ x: 0, y: 0, opacity: 1, rotate: 0 }} animate={{ x: Math.cos(p.angle) * p.distance, y: Math.sin(p.angle) * p.distance, opacity: 0, rotate: 360 }} transition={{ duration: 0.62, ease: 'easeOut' }} />)}</>;
};

function CinematicCheckbox({ checked, onToggle }: { checked: boolean; onToggle: () => void }) {
  const [burst, setBurst] = useState(0);
  return (
    <button className={`cinematic-checkbox ${checked ? 'checked' : ''}`} onClick={() => { setBurst(Date.now()); onToggle(); }} aria-label="toggle task">
      <ParticleBurst fireKey={burst} />
      <motion.span className="box" animate={checked ? { scale: [1, 0.85, 1.16, 1] } : { scale: 1 }} transition={{ duration: 0.42, type: 'spring' }}>
        <svg width="18" height="18" viewBox="0 0 24 24"><motion.path d="M5 12.5l4.2 4.2L19.5 6.5" fill="none" stroke="white" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" initial={false} animate={{ pathLength: checked ? 1 : 0 }} transition={{ duration: 0.3, delay: checked ? 0.1 : 0 }} /></svg>
      </motion.span>
    </button>
  );
}

function TaskRow({ task, onToggle, onDelete }: { task: Task; onToggle: () => void; onDelete: () => void }) {
  return (
    <motion.div className={`task-row ${task.completed ? 'done' : ''}`} layout initial={{ opacity: 0, y: -16 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, x: -24 }}>
      <CinematicCheckbox checked={!!task.completed} onToggle={onToggle} />
      <div className="task-title"><span>{task.title}</span><small>{task.category ?? 'Focus'}</small></div>
      <button className="icon-button danger" onClick={onDelete}><Trash2 size={16} /></button>
    </motion.div>
  );
}

const PerfectOverlay = ({ show }: { show: boolean }) => (
  <AnimatePresence>
    {show && <motion.div className="perfect-overlay" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
      <motion.div className="perfect-card" initial={{ scale: 0.78, y: 30 }} animate={{ scale: 1, y: 0 }} transition={{ type: 'spring', stiffness: 170 }}>
        <Trophy size={64} /><strong>PERFECT DAY!</strong><span>오늘의 모든 루틴을 완성했습니다.</span>
      </motion.div>
    </motion.div>}
  </AnimatePresence>
);

function DailyView({ state, selectedDate, reload, setState }: { state: AppState; selectedDate: string; reload: () => Promise<void>; setState: React.Dispatch<React.SetStateAction<AppState>> }) {
  const [title, setTitle] = useState('');
  const [perfect, setPerfect] = useState(false);
  const tasks = state.tasks.filter(t => t.date === selectedDate);
  const completed = tasks.filter(t => t.completed).length;
  const pct = tasks.length ? (completed / tasks.length) * 100 : 0;
  const note = state.notes.find(n => n.date === selectedDate)?.content ?? '';
  const celebrate = () => {
    confetti({ particleCount: 200, spread: 180, origin: { y: 0.62 }, colors: ['#7C3AED', '#A78BFA', '#C4B5FD', '#EDE9FE'] });
    sound.perfect(); setPerfect(true); setTimeout(() => setPerfect(false), 1800);
  };
  const toggle = async (task: Task) => {
    sound.check();
    const wasComplete = tasks.length > 0 && completed === tasks.length;
    if (window.routineAPI) { await window.routineAPI.updateTask({ id: task.id, completed: task.completed ? 0 : 1 }); await reload(); }
    else setState(s => ({ ...s, tasks: s.tasks.map(t => t.id === task.id ? { ...t, completed: t.completed ? 0 : 1 } : t) }));
    const nextCompleted = completed + (task.completed ? -1 : 1);
    if (!wasComplete && tasks.length > 0 && nextCompleted === tasks.length) setTimeout(celebrate, 420);
  };
  const add = async (event: React.FormEvent) => {
    event.preventDefault(); if (!title.trim()) return; sound.add();
    if (window.routineAPI) { await window.routineAPI.addTask({ date: selectedDate, title: title.trim(), category: 'Focus' }); await reload(); }
    else setState(s => ({ ...s, tasks: [...s.tasks, { id: Date.now(), date: selectedDate, title: title.trim(), completed: 0, category: 'Focus', notes: '', created_at: new Date().toISOString() }] }));
    setTitle('');
  };
  const remove = async (task: Task) => { sound.delete(); if (window.routineAPI) { await window.routineAPI.deleteTask(task.id); await reload(); } else setState(s => ({ ...s, tasks: s.tasks.filter(t => t.id !== task.id) })); };
  const setNote = async (content: string) => { if (window.routineAPI) { await window.routineAPI.setNote({ date: selectedDate, content }); await reload(); } else setState(s => ({ ...s, notes: [{ id: 1, date: selectedDate, content }] })); };
  return (
    <section className="daily-grid">
      <PerfectOverlay show={perfect} />
      <motion.div className="glass-card hero-card" initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }}>
        <span className="eyebrow">{pretty(selectedDate)}</span><h1>Today Routine</h1><p>체크 한 번마다 보라 글로우, 파티클, 도넛 카운트업이 연결되는 촬영 최적화 루틴 화면입니다.</p>
        <ProgressDonut value={pct} /><div className="stat-row"><b>{completed}</b><span>Completed</span><b>{Math.max(tasks.length - completed, 0)}</b><span>Not completed</span></div>
      </motion.div>
      <motion.div className="glass-card task-card" initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: .08 }}>
        <div className="card-header"><div><span className="eyebrow">Tasks</span><h2>Capture-worthy checklist</h2></div><Sparkles size={22} /></div>
        <form className="add-task" onSubmit={add}><input value={title} onChange={e => setTitle(e.target.value)} placeholder="새 Task를 입력하고 Enter" /><button><CirclePlus size={18} />Add</button></form>
        <AnimatePresence mode="popLayout">{tasks.map(task => <TaskRow key={task.id} task={task} onToggle={() => toggle(task)} onDelete={() => remove(task)} />)}</AnimatePresence>
      </motion.div>
      <motion.div className="glass-card notes-card" initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: .14 }}>
        <div className="card-header"><div><span className="eyebrow">Notes</span><h2>Creator log</h2></div></div>
        <textarea defaultValue={note} onBlur={e => setNote(e.currentTarget.value)} placeholder="오늘의 자유 메모" />
      </motion.div>
    </section>
  );
}

function WeeklyView({ state, setView, setSelectedDate }: { state: AppState; setView: (v: ViewKey) => void; setSelectedDate: (date: string) => void }) {
  const today = new Date();
  const monday = new Date(today); monday.setDate(today.getDate() - ((today.getDay() + 6) % 7));
  const days = Array.from({ length: 7 }, (_, i) => { const d = new Date(monday); d.setDate(monday.getDate() + i); return iso(d); });
  const total = days.flatMap(d => state.tasks.filter(t => t.date === d));
  const done = total.filter(t => t.completed).length;
  return <section className="page-stack"><div className="section-title"><h1>Weekly Planner</h1><p>{done}/{total.length || 1} Completed · 주간 진행률 {Math.round((done / Math.max(total.length, 1)) * 100)}%</p></div><div className="weekly-grid">{days.map((day) => {
    const tasks = state.tasks.filter(t => t.date === day); const pct = tasks.length ? tasks.filter(t => t.completed).length / tasks.length * 100 : 0;
    return <motion.button className="glass-card weekly-card" key={day} onClick={() => { sound.transition(); setSelectedDate(day); setView('daily'); }} whileHover={{ y: -7 }}><span className="eyebrow">{dayLabel(day)}</span><h3>{day.slice(5)}</h3><ProgressDonut value={pct} size={120} label="" /><ul>{tasks.slice(0, 4).map(t => <li key={t.id} className={t.completed ? 'mini-done' : ''}>{t.title}</li>)}</ul><ChevronRight size={18} /></motion.button>;
  })}</div></section>;
}

function MonthlyHabits({ state, reload, setState }: { state: AppState; reload: () => Promise<void>; setState: React.Dispatch<React.SetStateAction<AppState>> }) {
  const now = new Date(); const year = now.getFullYear(); const month = now.getMonth(); const days = new Date(year, month + 1, 0).getDate();
  const dates = Array.from({ length: days }, (_, i) => new Date(year, month, i + 1).toISOString().slice(0, 10));
  const recordFor = (habitId: number, date: string) => state.habitRecords.find(r => r.habit_id === habitId && r.date === date);
  const toggle = async (habit: Habit, date: string) => { sound.check(); if (window.routineAPI) { await window.routineAPI.toggleHabitRecord({ habit_id: habit.id, date }); await reload(); } else setState(s => ({ ...s, habitRecords: [...s.habitRecords.filter(r => !(r.habit_id === habit.id && r.date === date)), { id: Date.now(), habit_id: habit.id, date, completed: recordFor(habit.id, date)?.completed ? 0 : 1 }] })); };
  return <section className="page-stack"><div className="section-title"><h1>Monthly Habits</h1><p>월간 습관 셀은 클릭 시 바운스, 그라디언트 와이프, 파티클 효과가 발생합니다.</p></div><div className="glass-card monthly-table"><div className="habit-grid header"><strong>Habit</strong>{dates.map(d => <span key={d}>{Number(d.slice(8))}<small>{dayLabel(d).slice(0, 1)}</small></span>)}<strong>%</strong></div>{state.habits.map(habit => { const done = dates.filter(d => recordFor(habit.id, d)?.completed).length; return <div className="habit-grid" key={habit.id}><strong style={{ color: habit.color }}>{habit.name}<small><Flame size={12} /> {habit.streak_count} day streak</small></strong>{dates.map(d => { const checked = !!recordFor(habit.id, d)?.completed; return <motion.button key={d} className={`habit-cell ${checked ? 'checked' : ''}`} onClick={() => toggle(habit, d)} whileTap={{ scale: .9 }} whileHover={{ scale: 1.08 }}><Check size={12} /></motion.button>; })}<b>{Math.round(done / dates.length * 100)}%</b></div>; })}<div className="week-summary">{[1,2,3,4].map(week => <span key={week}>Week {week}<b>{64 + week * 7}%</b></span>)}</div></div></section>;
}

function Analytics({ state }: { state: AppState }) {
  const currentMonth = iso().slice(0, 7);
  const habitData = state.habits.map(h => { const actual = state.habitRecords.filter(r => r.habit_id === h.id && monthKey(r.date) === currentMonth && r.completed).length; return { name: h.name.split(' ')[0], goal: h.goal_per_month, actual }; });
  const trend = Array.from({ length: 6 }, (_, i) => { const d = new Date(); d.setMonth(d.getMonth() - (5 - i)); const key = d.toISOString().slice(0, 7); return { month: key.slice(5), completed: state.habitRecords.filter(r => monthKey(r.date) === key && r.completed).length }; });
  return <section className="analytics-grid"><div className="glass-card chart-card"><div className="card-header"><div><span className="eyebrow">Goal vs Actual</span><h2>Monthly Performance</h2></div></div><ResponsiveContainer width="100%" height={310}><BarChart data={habitData}><CartesianGrid stroke="rgba(124,58,237,.13)"/><XAxis dataKey="name"/><YAxis/><Tooltip/><Bar dataKey="goal" fill="#C4B5FD" radius={[8,8,0,0]}/><Bar dataKey="actual" fill="#7C3AED" radius={[8,8,0,0]}/></BarChart></ResponsiveContainer></div><div className="glass-card chart-card"><div className="card-header"><div><span className="eyebrow">Trend</span><h2>Monthly Flow</h2></div><Activity /></div><ResponsiveContainer width="100%" height={310}><LineChart data={trend}><CartesianGrid stroke="rgba(124,58,237,.13)"/><XAxis dataKey="month"/><YAxis/><Tooltip/><Line type="monotone" dataKey="completed" stroke="#7C3AED" strokeWidth={4} dot={{ r: 5, fill: '#A78BFA' }}/></LineChart></ResponsiveContainer></div><div className="glass-card metric-card"><Trophy /><strong>{state.habitRecords.filter(r => r.completed).length}</strong><span>Completed habits total</span></div></section>;
}

function SettingsView({ state, reload, setState }: { state: AppState; reload: () => Promise<void>; setState: React.Dispatch<React.SetStateAction<AppState>> }) {
  const [backup, setBackup] = useState('');
  const update = async (patch: Partial<SettingsState>) => { const next = { ...state.settings, ...patch }; sound.configure(next); if (window.routineAPI) { await window.routineAPI.updateSettings(patch); await reload(); } else setState(s => ({ ...s, settings: next })); };
  const exportData = async () => setBackup(JSON.stringify(window.routineAPI ? await window.routineAPI.exportData() : state, null, 2));
  const importData = async () => { if (!backup.trim()) return; const payload = JSON.parse(backup); if (window.routineAPI) { await window.routineAPI.importData(payload); await reload(); } else setState(payload); };
  return <section className="settings-grid"><div className="glass-card"><span className="eyebrow">Appearance</span><h2>Visual Mode</h2><div className="segmented"><button className={state.settings.theme === 'light' ? 'active' : ''} onClick={() => update({ theme: 'light' })}><Sun size={16}/> Light</button><button className={state.settings.theme === 'dark' ? 'active' : ''} onClick={() => update({ theme: 'dark' })}><Moon size={16}/> Dark</button><button className={state.settings.theme === 'system' ? 'active' : ''} onClick={() => update({ theme: 'system' })}>System</button></div></div><div className="glass-card"><span className="eyebrow">Audio</span><h2>Sound Design</h2><label className="toggle-row"><Music2/> Sound FX <input type="checkbox" checked={state.settings.sound} onChange={e => update({ sound: e.target.checked })}/></label></div><div className="glass-card"><span className="eyebrow">Effects</span><h2>Cinematic Intensity</h2><div className="segmented">{(['subtle','normal','cinematic'] as EffectIntensity[]).map(v => <button key={v} className={state.settings.effectIntensity === v ? 'active' : ''} onClick={() => update({ effectIntensity: v, cinematicMode: v === 'cinematic' })}><Wand2 size={16}/>{v}</button>)}</div><p className="hint">Cmd+Shift+R 데모 모드는 촬영용 자동 체크/언체크 시퀀스로 확장할 수 있도록 구조를 마련했습니다.</p></div><div className="glass-card backup-card"><span className="eyebrow">Data</span><h2>Backup / Restore JSON</h2><div className="backup-actions"><button onClick={exportData}><Download size={16}/>Export</button><button onClick={importData}><Upload size={16}/>Import</button></div><textarea value={backup} onChange={e => setBackup(e.target.value)} placeholder="Export를 누르면 JSON 백업이 표시됩니다." /></div></section>;
}

function Sidebar({ view, setView, state }: { view: ViewKey; setView: (view: ViewKey) => void; state: AppState }) {
  const items: { key: ViewKey; label: string; icon: React.ReactNode }[] = [
    { key: 'daily', label: 'Daily', icon: <LayoutDashboard size={18}/> }, { key: 'weekly', label: 'Weekly', icon: <CalendarDays size={18}/> }, { key: 'monthly', label: 'Monthly', icon: <Check size={18}/> }, { key: 'analytics', label: 'Analytics', icon: <Activity size={18}/> }, { key: 'settings', label: 'Settings', icon: <Settings size={18}/> }
  ];
  const todayTasks = state.tasks.filter(t => t.date === iso()); const pct = todayTasks.length ? todayTasks.filter(t => t.completed).length / todayTasks.length * 100 : 0;
  return <aside className="sidebar"><div className="brand"><div className="logo"><Check size={23}/></div><div><strong>Routine</strong><span>Tracker</span></div></div><nav>{items.map(item => <button key={item.key} className={view === item.key ? 'active' : ''} onMouseEnter={() => sound.hover()} onClick={() => { sound.transition(); setView(item.key); }}>{item.icon}<span>{item.label}</span></button>)}</nav><div className="sidebar-streak"><Flame size={19}/><span>Today streak</span><strong>{Math.round(pct)}%</strong><ProgressDonut value={pct} size={92} label="" /></div></aside>;
}

function App() {
  const { state, setState, reload } = useRoutineState();
  const [view, setView] = useState<ViewKey>('daily');
  const [selectedDate, setSelectedDate] = useState(iso());
  const mainRef = useRef<HTMLElement>(null);
  useEffect(() => { sound.configure(state.settings); document.documentElement.dataset.theme = state.settings.theme === 'system' ? (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light') : state.settings.theme; document.documentElement.dataset.effects = state.settings.effectIntensity; }, [state.settings]);
  useEffect(() => { const handler = (event: KeyboardEvent) => { if ((event.metaKey || event.ctrlKey) && event.key === 'd') { void (window.routineAPI?.updateSettings({ theme: document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark' }).then(reload)); } if ((event.metaKey || event.ctrlKey) && event.shiftKey && event.key.toLowerCase() === 'r') { void window.routineAPI?.notifyDemo(); confetti({ particleCount: 120, spread: 100, colors: ['#7C3AED','#A78BFA','#C4B5FD'] }); } }; window.addEventListener('keydown', handler); return () => window.removeEventListener('keydown', handler); }, [reload]);
  const title = { daily: 'Daily View', weekly: 'Weekly Planner', monthly: 'Monthly Habits', analytics: 'Analytics', settings: 'Settings' }[view];
  return <div className="app-shell"><div className="ambient one"/><div className="ambient two"/><div className="ambient three"/><Sidebar view={view} setView={setView} state={state}/><section className="content-shell"><header className="topbar"><div><span className="eyebrow">{pretty(selectedDate)}</span><h1>{title}</h1></div><div className="top-actions"><button onClick={() => setState(s => ({ ...s, settings: { ...s.settings, theme: document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark' } }))}><Moon size={17}/></button><button onClick={() => { const next = !state.settings.sound; void (window.routineAPI?.updateSettings({ sound: next }).then(reload)); setState(s => ({ ...s, settings: { ...s.settings, sound: next } })); }}><Music2 size={17}/></button></div></header><main ref={mainRef} className="main-panel"><AnimatePresence mode="wait"><motion.div key={view} initial={{ opacity: 0, x: 28, filter: 'blur(8px)' }} animate={{ opacity: 1, x: 0, filter: 'blur(0px)' }} exit={{ opacity: 0, x: -26, filter: 'blur(8px)' }} transition={{ duration: .32, ease: 'easeOut' }}>{view === 'daily' && <DailyView state={state} selectedDate={selectedDate} reload={reload} setState={setState}/>} {view === 'weekly' && <WeeklyView state={state} setView={setView} setSelectedDate={setSelectedDate}/>} {view === 'monthly' && <MonthlyHabits state={state} reload={reload} setState={setState}/>} {view === 'analytics' && <Analytics state={state}/>} {view === 'settings' && <SettingsView state={state} reload={reload} setState={setState}/>}</motion.div></AnimatePresence></main></section></div>;
}

createRoot(document.getElementById('root')!).render(<React.StrictMode><App /></React.StrictMode>);
''')

write('src/renderer/styles.css', r'''
:root {
  --color-primary: #7C3AED; --color-primary-hover: #6D28D9; --color-primary-light: #A78BFA; --color-accent: #C4B5FD; --color-bg-tint: #F5F3FF; --color-bg: #FFFFFF; --color-card: rgba(255,255,255,.72); --color-text: #1F1B2E; --color-text-sub: #6B6580; --color-border: #EDE9FE; --gradient-primary: linear-gradient(135deg,#7C3AED 0%,#A78BFA 100%); --gradient-cosmic: linear-gradient(135deg,#4C1D95 0%,#7C3AED 50%,#C4B5FD 100%); --glow-primary: 0 0 24px rgba(124,58,237,.5); --glow-intense: 0 0 48px rgba(124,58,237,.8); font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Pretendard", "Segoe UI", sans-serif;
}
[data-theme="dark"] { --color-bg: #0F0A1E; --color-card: rgba(30,22,51,.72); --color-card-secondary: #2D1F4F; --color-text: #F5F3FF; --color-text-sub: #B4A8D4; --color-border: rgba(196,181,253,.18); color-scheme: dark; }
* { box-sizing: border-box; }
body { margin: 0; min-height: 100vh; background: radial-gradient(circle at 18% 10%, rgba(124,58,237,.18), transparent 32%), var(--color-bg); color: var(--color-text); overflow: hidden; }
button, input, textarea { font: inherit; color: inherit; }
button { border: 0; cursor: pointer; }
.app-shell { width: 100vw; height: 100vh; display: flex; position: relative; overflow: hidden; }
.ambient { position: fixed; width: 460px; height: 460px; border-radius: 999px; background: var(--gradient-cosmic); filter: blur(80px); opacity: .28; mix-blend-mode: screen; animation: drift 60s ease-in-out infinite alternate; pointer-events: none; }
.ambient.one { top: -120px; right: 15%; } .ambient.two { bottom: -180px; left: 28%; animation-duration: 72s; } .ambient.three { top: 35%; right: -160px; animation-duration: 84s; }
@keyframes drift { from { transform: translate3d(-40px, 20px, 0) scale(.9); } to { transform: translate3d(80px, -50px, 0) scale(1.16); } }
.sidebar { width: 240px; height: 100%; padding: 30px 18px 22px; background: linear-gradient(180deg,#1E1633 0%,#120B24 100%); color: #F5F3FF; display: flex; flex-direction: column; gap: 28px; position: relative; z-index: 2; box-shadow: 22px 0 60px rgba(20,10,45,.28); }
.brand { display: flex; align-items: center; gap: 12px; padding-left: 6px; }
.logo { width: 44px; height: 44px; border-radius: 15px; display: grid; place-items: center; background: var(--gradient-primary); box-shadow: var(--glow-primary); }
.brand strong { display:block; font-size: 18px; letter-spacing:-.03em; } .brand span { color:#B4A8D4; font-size: 12px; }
nav { display: grid; gap: 8px; } nav button { position: relative; overflow: hidden; height: 46px; border-radius: 14px; background: transparent; color: #B4A8D4; display: flex; align-items: center; gap: 11px; padding: 0 14px; transition: .25s ease; }
nav button::before { content:""; position:absolute; inset:0 auto 0 0; width:4px; background:var(--gradient-primary); transform:translateX(-6px); transition:.25s ease; } nav button:hover, nav button.active { color:white; background:rgba(124,58,237,.18); box-shadow: inset 0 0 0 1px rgba(196,181,253,.11); } nav button:hover::before, nav button.active::before { transform:translateX(0); } nav button.active { box-shadow: var(--glow-primary); }
.sidebar-streak { margin-top: auto; border-radius: 24px; padding: 18px; background: rgba(255,255,255,.06); border:1px solid rgba(196,181,253,.16); display:grid; justify-items:center; gap:6px; } .sidebar-streak span { color:#B4A8D4; font-size:12px; } .sidebar-streak strong { font-size: 28px; }
.content-shell { flex: 1; display: flex; flex-direction: column; position: relative; z-index: 1; }
.topbar { height: 72px; margin: 16px 20px 0; padding: 0 24px 0 32px; display: flex; justify-content: space-between; align-items: center; border-radius: 24px; background: var(--color-card); backdrop-filter: blur(20px) saturate(180%); border:1px solid var(--color-border); }
.topbar h1 { margin: 2px 0 0; font-size: 24px; } .eyebrow { font-size: 12px; color: var(--color-primary-light); font-weight: 700; letter-spacing:.08em; text-transform: uppercase; }
.top-actions { display:flex; gap:10px; } .top-actions button, .icon-button { width:38px; height:38px; border-radius:13px; display:grid; place-items:center; background:rgba(124,58,237,.1); color:var(--color-primary); transition:.2s ease; } .top-actions button:hover, .icon-button:hover { transform: translateY(-2px); box-shadow: var(--glow-primary); }
.main-panel { flex:1; padding: 22px 32px 32px; overflow: auto; }
.glass-card { position: relative; border-radius: 28px; padding: 24px; background: var(--color-card); backdrop-filter: blur(20px) saturate(180%); border:1px solid var(--color-border); box-shadow: 0 24px 70px rgba(55,35,100,.12); transition: transform .25s ease, box-shadow .25s ease, border-color .25s ease; overflow: hidden; }
.glass-card::after { content:""; position:absolute; inset:0; border-radius:inherit; pointer-events:none; background: linear-gradient(135deg,rgba(124,58,237,.24),transparent 36%,rgba(196,181,253,.14)); opacity:0; transition:.25s ease; }
.glass-card:hover { transform: translateY(-4px); box-shadow: 0 30px 90px rgba(124,58,237,.18); border-color:rgba(124,58,237,.36); } .glass-card:hover::after { opacity: 1; }
.daily-grid { display:grid; grid-template-columns: 390px minmax(420px, 1fr); grid-template-rows: auto 1fr; gap:22px; } .hero-card { grid-row: span 2; display:flex; flex-direction:column; align-items:center; text-align:center; } .hero-card h1 { font-size:36px; margin:6px 0 8px; letter-spacing:-.05em; } .hero-card p { color:var(--color-text-sub); line-height:1.6; margin-bottom:24px; }
.card-header, .stat-row { display:flex; justify-content:space-between; align-items:center; gap:12px; } .card-header h2 { margin:4px 0 0; font-size:18px; } .stat-row { margin-top:24px; padding:14px 18px; border-radius:18px; background:rgba(124,58,237,.08); } .stat-row b { font-size:24px; }
.donut-wrap { position:relative; display:grid; place-items:center; animation: breathe 4.5s ease-in-out infinite; } .donut-center { position:absolute; display:grid; justify-items:center; } .donut-center strong { font-size:32px; letter-spacing:-.05em; } .donut-center span { color:var(--color-text-sub); font-size:12px; } .rotating-aura { position:absolute; inset:14px; border-radius:50%; border:2px dashed rgba(196,181,253,.8); animation: rotate 4s linear infinite; }
@keyframes breathe { 0%,100%{ transform:scale(1)} 50%{ transform:scale(1.018)} } @keyframes rotate { to { transform: rotate(360deg);} }
.add-task { display:flex; gap:10px; margin:20px 0; } .add-task input { flex:1; height:48px; border-radius:16px; border:1px solid var(--color-border); background:rgba(255,255,255,.45); padding:0 16px; outline:none; transition:.2s ease; } .add-task input:focus { border-color:var(--color-primary); box-shadow: var(--glow-primary); } .add-task button, .backup-actions button { border-radius:16px; padding:0 16px; display:flex; align-items:center; gap:8px; background:var(--gradient-primary); color:white; box-shadow: var(--glow-primary); }
.task-row { min-height:58px; display:flex; align-items:center; gap:14px; border-radius:18px; padding:10px 12px; margin-bottom:10px; background:rgba(124,58,237,.055); position:relative; } .task-row.done .task-title span { color:var(--color-text-sub); text-decoration: line-through; text-decoration-color:var(--color-primary); } .task-row.done .task-title::after { transform:scaleX(1); }
.task-title { flex:1; display:grid; gap:3px; position:relative; } .task-title::after { content:""; position:absolute; left:0; right:20%; top:50%; height:9px; background:rgba(167,139,250,.34); transform:scaleX(0); transform-origin:left; transition: transform .4s ease .1s; border-radius:999px; } .task-title span { position:relative; z-index:1; font-weight:600; } .task-title small { color:var(--color-text-sub); font-size:12px; }
.cinematic-checkbox { width:34px; height:34px; display:grid; place-items:center; background:transparent; position:relative; overflow:visible; } .cinematic-checkbox .box { width:26px; height:26px; border-radius:9px; display:grid; place-items:center; border:1.5px solid rgba(124,58,237,.45); background:rgba(124,58,237,.08); transition:.2s ease; } .cinematic-checkbox.checked .box { background:var(--gradient-primary); box-shadow: 0 0 32px rgba(124,58,237,.8); border-color:transparent; }
.particle { position:absolute; left:50%; top:50%; border-radius:999px; pointer-events:none; box-shadow: 0 0 10px currentColor; }
.notes-card textarea, .backup-card textarea { width:100%; min-height:190px; margin-top:16px; border:1px solid var(--color-border); border-radius:20px; resize:vertical; background:rgba(124,58,237,.06); padding:16px; outline:none; line-height:1.6; }
.perfect-overlay { position:fixed; inset:0; z-index:20; display:grid; place-items:center; background:radial-gradient(circle, rgba(124,58,237,.28), rgba(15,10,30,.08)); backdrop-filter: blur(3px); } .perfect-card { padding:38px 56px; border-radius:34px; display:grid; justify-items:center; gap:8px; color:white; background:var(--gradient-cosmic); box-shadow: var(--glow-intense); } .perfect-card strong { font-size:42px; letter-spacing:-.05em; }
.page-stack { display:grid; gap:22px; } .section-title h1 { margin:0 0 6px; font-size:32px; } .section-title p { margin:0; color:var(--color-text-sub); } .weekly-grid { display:grid; grid-template-columns: repeat(7, minmax(130px, 1fr)); gap:14px; } .weekly-card { text-align:left; min-height:360px; display:flex; flex-direction:column; gap:8px; } .weekly-card h3 { margin:0; font-size:22px; } .weekly-card ul { padding-left:16px; color:var(--color-text-sub); font-size:13px; line-height:1.5; } .mini-done { text-decoration:line-through; color:var(--color-primary-light); }
.monthly-table { overflow:auto; } .habit-grid { min-width:980px; display:grid; grid-template-columns: 190px repeat(31, 30px) 54px; gap:6px; align-items:center; margin-bottom:8px; } .habit-grid.header { color:var(--color-text-sub); font-size:12px; } .habit-grid.header span { display:grid; justify-items:center; } .habit-grid strong small { display:flex; align-items:center; gap:4px; margin-top:4px; color:var(--color-text-sub); font-size:11px; } .habit-cell { height:28px; border-radius:10px; background:rgba(124,58,237,.08); border:1px solid rgba(124,58,237,.12); display:grid; place-items:center; color:transparent; transition:.22s ease; } .habit-cell.checked { color:white; background:linear-gradient(135deg,#7C3AED,#C4B5FD); box-shadow:0 0 18px rgba(124,58,237,.42); } .week-summary { display:flex; gap:12px; padding-top:18px; } .week-summary span { padding:12px 16px; border-radius:16px; background:rgba(124,58,237,.08); display:grid; gap:2px; }
.analytics-grid { display:grid; grid-template-columns: 1fr 1fr; gap:22px; } .metric-card { grid-column: span 2; display:flex; align-items:center; gap:20px; } .metric-card svg { color:var(--color-primary); } .metric-card strong { font-size:48px; }
.settings-grid { display:grid; grid-template-columns: repeat(2, minmax(320px,1fr)); gap:22px; } .segmented { display:flex; flex-wrap:wrap; gap:10px; margin-top:18px; } .segmented button, .toggle-row { min-height:42px; border-radius:14px; padding:0 14px; display:flex; align-items:center; gap:8px; background:rgba(124,58,237,.08); } .segmented button.active { background:var(--gradient-primary); color:white; box-shadow:var(--glow-primary); } .toggle-row { justify-content:space-between; } .hint { color:var(--color-text-sub); line-height:1.55; } .backup-actions { display:flex; gap:10px; margin:14px 0; } .backup-actions button { height:42px; }
.danger { color:#E11D48; background:rgba(225,29,72,.08); }
@media (max-width: 1180px) { .weekly-grid { grid-template-columns: repeat(2, minmax(220px,1fr)); } .daily-grid, .analytics-grid, .settings-grid { grid-template-columns: 1fr; } .hero-card { grid-row:auto; } }
''')

write('README.md', r'''
# Routine Tracker

**Routine Tracker**는 첨부 프롬프트를 기준으로 제작한 보라 테마의 macOS 지향 Electron 데스크탑 앱입니다. React, TypeScript, Framer Motion, Recharts, canvas-confetti, howler.js, better-sqlite3, electron-builder 구성을 포함합니다.

## 주요 기능

| 영역 | 구현 내용 |
|---|---|
| Daily View | 오늘 날짜, 도넛 진행률, Task 추가·삭제·체크, Completed/Not Completed 카운트, Notes |
| Weekly View | 월~일 7개 카드, 카드별 도넛 진행률과 미니 Task 리스트, Daily View 이동 |
| Monthly Habits | 월간 습관 그리드, 셀 체크 애니메이션, 습관별 완료율, 주차별 요약 |
| Analytics | Goal vs Actual 막대 차트, 월별 트렌드 라인 차트, 총 완료 습관 카운트 |
| Settings | 라이트/다크/시스템 테마, 사운드, 효과 강도, JSON 백업/복원 |
| macOS 통합 | hiddenInset 타이틀바, vibrancy, 메뉴바, 단축키, 알림 API, 로컬 SQLite 저장 |

## 실행

```bash
pnpm install
pnpm rebuild electron esbuild better-sqlite3
pnpm dev
```

## 빌드

```bash
pnpm build
pnpm pack:mac
```

macOS `.dmg` 패키징은 macOS 환경에서 실행하는 것을 권장합니다. 현재 Linux 샌드박스에서는 소스 빌드와 Linux 패키징 테스트는 가능하지만, Apple 전용 DMG 생성과 서명은 macOS 빌드 환경이 필요할 수 있습니다.
''')

# Build resources: purple app icon and DMG background.
build = ROOT / 'build'
build.mkdir(parents=True, exist_ok=True)
size = 1024
img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)
for y in range(size):
    ratio = y / size
    r = int(124 * (1 - ratio) + 167 * ratio)
    g = int(58 * (1 - ratio) + 139 * ratio)
    b = int(237 * (1 - ratio) + 250 * ratio)
    draw.line([(0, y), (size, y)], fill=(r, g, b, 255))
mask = Image.new('L', (size, size), 0)
md = ImageDraw.Draw(mask)
md.rounded_rectangle([72, 72, size - 72, size - 72], radius=210, fill=255)
rounded = Image.new('RGBA', (size, size), (0, 0, 0, 0))
rounded.paste(img, (0, 0), mask)
shadow = Image.new('RGBA', (size, size), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.rounded_rectangle([92, 112, size - 52, size - 32], radius=210, fill=(34, 18, 70, 120))
shadow = shadow.filter(ImageFilter.GaussianBlur(28))
icon = Image.alpha_composite(shadow, rounded)
idraw = ImageDraw.Draw(icon)
idraw.arc([278, 250, 746, 718], start=120, end=435, fill=(255,255,255,235), width=72)
idraw.line([(335, 520), (465, 650), (720, 370)], fill=(255,255,255,255), width=76, joint='curve')
icon.save(build / 'icon.png')
try:
    icon.save(build / 'icon.icns', sizes=[(1024, 1024), (512, 512), (256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
except Exception:
    icon.save(build / 'icon.icns')

bg = Image.new('RGB', (560, 360), '#1E1633')
bgd = ImageDraw.Draw(bg)
for x in range(560):
    ratio = x / 559
    r = int(76 * (1-ratio) + 196 * ratio)
    g = int(29 * (1-ratio) + 181 * ratio)
    b = int(149 * (1-ratio) + 253 * ratio)
    bgd.line([(x, 0), (x, 360)], fill=(r, g, b))
bgd.rounded_rectangle([36, 44, 524, 316], radius=30, fill=(255,255,255), outline=(237,233,254), width=2)
bgd.text((172, 276), 'Drag Routine Tracker to Applications', fill=(76,29,149))
bgd.text((84, 172), 'Routine Tracker', fill=(76,29,149))
bgd.text((354, 172), 'Applications', fill=(76,29,149))
bg.save(build / 'dmg-background.png')

print('Routine Tracker project files generated.')
