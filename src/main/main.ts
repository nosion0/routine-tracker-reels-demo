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
    ['90분 깊은 집중 작업', 1, 'Focus'],
    ['아침 스트레칭과 물 마시기', 1, 'Health'],
    ['창의 콘셉트 초안 작성', 0, 'Creation'],
    ['받은 편지함 정리', 0, 'Admin'],
    ['책 15쪽 읽기', 0, 'Growth'],
    ['내일 준비 계획하기', 0, 'Planning']
  ];
  for (const [title, completed, category] of samples) taskInsert.run(todayISO(), title, completed, category, '', nowISO());
  for (let offset = -3; offset <= 6; offset++) {
    if (offset === 0) continue;
    taskInsert.run(todayISO(offset), '유용한 아이디어 하나 기록하기', Math.random() > 0.35 ? 1 : 0, 'Creation', '', nowISO());
    taskInsert.run(todayISO(offset), '20분 몸 움직이기', Math.random() > 0.45 ? 1 : 0, 'Health', '', nowISO());
    taskInsert.run(todayISO(offset), '무스크롤 집중 블록', Math.random() > 0.5 ? 1 : 0, 'Focus', '', nowISO());
  }

  const habitInsert = db.prepare('INSERT INTO habits (name, goal_per_month, color, streak_count, created_at) VALUES (?, ?, ?, ?, ?)');
  const habitIds = [
    habitInsert.run('깊은 창작 작업', 24, '#7C3AED', 7, nowISO()).lastInsertRowid,
    habitInsert.run('운동', 20, '#A78BFA', 4, nowISO()).lastInsertRowid,
    habitInsert.run('독서', 26, '#C4B5FD', 12, nowISO()).lastInsertRowid,
    habitInsert.run('무설탕', 18, '#8B5CF6', 3, nowISO()).lastInsertRowid,
    habitInsert.run('저녁 회고', 22, '#DDD6FE', 8, nowISO()).lastInsertRowid
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
      new Notification({ title: '루틴 트래커', body: '오늘의 루틴 시작! 보라색 몰입 모드가 준비되었습니다.' }).show();
    }
    return { ok: true };
  });
}

function buildMenu() {
  const template: Electron.MenuItemConstructorOptions[] = [
    {
      label: '루틴 트래커',
      submenu: [
        { role: 'about' },
        { type: 'separator' },
        { label: '사용자 데이터 열기', click: () => shell.openPath(app.getPath('userData')) },
        { type: 'separator' },
        { role: 'quit' }
      ]
    },
    {
      label: '파일',
      submenu: [
        { label: '새 할 일', accelerator: 'CommandOrControl+N', click: () => mainWindow?.webContents.send('shortcut:new-task') },
        { type: 'separator' },
        { role: 'close' }
      ]
    },
    { label: '편집', submenu: [{ role: 'undo' }, { role: 'redo' }, { type: 'separator' }, { role: 'cut' }, { role: 'copy' }, { role: 'paste' }] },
    {
      label: '보기',
      submenu: [
        { label: '일간', accelerator: 'CommandOrControl+1', click: () => mainWindow?.webContents.send('shortcut:view', 'daily') },
        { label: '주간', accelerator: 'CommandOrControl+2', click: () => mainWindow?.webContents.send('shortcut:view', 'weekly') },
        { label: '월간', accelerator: 'CommandOrControl+3', click: () => mainWindow?.webContents.send('shortcut:view', 'monthly') },
        { label: '분석', accelerator: 'CommandOrControl+4', click: () => mainWindow?.webContents.send('shortcut:view', 'analytics') },
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
