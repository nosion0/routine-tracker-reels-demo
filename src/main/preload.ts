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
