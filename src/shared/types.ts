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
