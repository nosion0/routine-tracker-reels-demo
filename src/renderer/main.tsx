import React, { useEffect, useMemo, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { AnimatePresence, motion } from 'framer-motion';
import confetti from 'canvas-confetti';
import {
  BarChart, Bar, CartesianGrid, Cell, Legend, Line, LineChart, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis
} from 'recharts';
import {
  Activity, CalendarDays, Check, ChevronRight, CirclePlus, Download, Flame, LayoutDashboard,
  Moon, Music2, Settings, Sparkles, Sun, Trash2, Trophy, Upload, Wand2
} from 'lucide-react';
import type { AppState, EffectIntensity, Habit, HabitRecord, SettingsState, Task, ViewKey } from '../shared/types';
import { sound } from './effects/sound';
import './styles.css';

const formatDateLocal = (date: Date) => {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
};
const iso = (date = new Date()) => formatDateLocal(date);
const pretty = (value: string) => new Date(`${value}T12:00:00`).toLocaleDateString('ko-KR', { weekday: 'long', month: '2-digit', day: '2-digit', year: 'numeric' });
const dayLabel = (value: string) => new Date(`${value}T12:00:00`).toLocaleDateString('ko-KR', { weekday: 'short' });
const dayInitial = (value: string) => dayLabel(value).replace('요일', '').slice(0, 1);
const monthKey = (value: string) => value.slice(0, 7);

const categoryMap: Record<string, string> = {
  Focus: '집중', Health: '건강', Creation: '창작', Admin: '관리', Growth: '성장', Planning: '계획'
};
const translateCategory = (category?: string | null) => categoryMap[category ?? 'Focus'] ?? category ?? '집중';

const fallbackState = (): AppState => {
  const today = iso();
  const tasks: Task[] = ['90분 깊은 집중 작업', '아침 스트레칭과 물 마시기', '창의 콘셉트 초안 작성', '받은 편지함 정리', '책 15쪽 읽기'].map((title, index) => ({
    id: index + 1,
    date: today,
    title,
    completed: index < 2 ? 1 : 0,
    category: ['Focus', 'Health', 'Creation', 'Admin', 'Growth'][index],
    notes: '',
    created_at: new Date().toISOString()
  }));
  const habits: Habit[] = ['깊은 창작 작업', '운동', '독서', '무설탕', '저녁 회고'].map((name, index) => ({
    id: index + 1,
    name,
    goal_per_month: 22 + index,
    color: ['#7C3AED', '#A78BFA', '#C4B5FD', '#8B5CF6', '#DDD6FE'][index],
    streak_count: 3 + index,
    created_at: new Date().toISOString()
  }));
  const records: HabitRecord[] = [];
  const now = new Date();
  const days = new Date(now.getFullYear(), now.getMonth() + 1, 0).getDate();
  habits.forEach((habit) => {
    for (let d = 1; d <= days; d += 1) {
      records.push({ id: habit.id * 100 + d, habit_id: habit.id, date: formatDateLocal(new Date(now.getFullYear(), now.getMonth(), d)), completed: d <= now.getDate() && (d + habit.id) % 3 !== 0 ? 1 : 0 });
    }
  });
  return {
    tasks,
    habits,
    habitRecords: records,
    notes: [{ id: 1, date: today, content: '브라우저 미리보기용 샘플 데이터입니다.' }],
    achievements: [],
    settings: { theme: 'system', sound: true, effectIntensity: 'cinematic', cinematicMode: true }
  };
};

function useRoutineState() {
  const [state, setState] = useState<AppState>(fallbackState());
  const reload = async () => {
    if (window.routineAPI) setState(await window.routineAPI.getState());
  };
  useEffect(() => { void reload(); }, []);
  return { state, setState, reload };
}

const ProgressDonut = ({ value, size = 190, label = '완료' }: { value: number; size?: number; label?: string }) => {
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
    id: `${fireKey}-${index}`,
    angle: (Math.PI * 2 * index) / 16,
    distance: 58 + Math.random() * 44,
    size: 4 + Math.random() * 5,
    color: ['#7C3AED', '#A78BFA', '#C4B5FD'][index % 3]
  })), [fireKey]);
  if (!fireKey) return null;
  return <>{particles.map((p) => <motion.span key={p.id} className="particle" style={{ width: p.size, height: p.size, background: p.color }} initial={{ x: 0, y: 0, opacity: 1, rotate: 0 }} animate={{ x: Math.cos(p.angle) * p.distance, y: Math.sin(p.angle) * p.distance, opacity: 0, rotate: 360 }} transition={{ duration: 0.62, ease: 'easeOut' }} />)}</>;
};

function CinematicCheckbox({ checked, onToggle, label = '체크 전환' }: { checked: boolean; onToggle: () => void; label?: string }) {
  const [burst, setBurst] = useState(0);
  return (
    <button className={`cinematic-checkbox ${checked ? 'checked' : ''}`} onClick={() => { setBurst(Date.now()); onToggle(); }} aria-label={label}>
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
      <CinematicCheckbox checked={!!task.completed} onToggle={onToggle} label={`${task.title} 완료 전환`} />
      <div className="task-title"><span>{task.title}</span><small>{translateCategory(task.category)}</small></div>
      <button className="icon-button danger" onClick={onDelete} aria-label={`${task.title} 삭제`}><Trash2 size={16} /></button>
    </motion.div>
  );
}

const PerfectOverlay = ({ show }: { show: boolean }) => (
  <AnimatePresence>
    {show && <motion.div className="perfect-overlay" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
      <motion.div className="perfect-card" initial={{ scale: 0.78, y: 30 }} animate={{ scale: 1, y: 0 }} transition={{ type: 'spring', stiffness: 170 }}>
        <Trophy size={64} /><strong>완벽한 하루!</strong><span>오늘의 모든 루틴을 완성했습니다.</span>
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
    sound.perfect();
    setPerfect(true);
    setTimeout(() => setPerfect(false), 1800);
  };
  const toggle = async (task: Task) => {
    sound.check();
    const wasComplete = tasks.length > 0 && completed === tasks.length;
    if (window.routineAPI) {
      await window.routineAPI.updateTask({ id: task.id, completed: task.completed ? 0 : 1 });
      await reload();
    } else {
      setState(s => ({ ...s, tasks: s.tasks.map(t => t.id === task.id ? { ...t, completed: t.completed ? 0 : 1 } : t) }));
    }
    const nextCompleted = completed + (task.completed ? -1 : 1);
    if (!wasComplete && tasks.length > 0 && nextCompleted === tasks.length) setTimeout(celebrate, 420);
  };
  const add = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!title.trim()) return;
    sound.add();
    if (window.routineAPI) {
      await window.routineAPI.addTask({ date: selectedDate, title: title.trim(), category: 'Focus' });
      await reload();
    } else {
      setState(s => ({ ...s, tasks: [...s.tasks, { id: Date.now(), date: selectedDate, title: title.trim(), completed: 0, category: 'Focus', notes: '', created_at: new Date().toISOString() }] }));
    }
    setTitle('');
  };
  const remove = async (task: Task) => {
    sound.delete();
    if (window.routineAPI) {
      await window.routineAPI.deleteTask(task.id);
      await reload();
    } else {
      setState(s => ({ ...s, tasks: s.tasks.filter(t => t.id !== task.id) }));
    }
  };
  const setNote = async (content: string) => {
    if (window.routineAPI) {
      await window.routineAPI.setNote({ date: selectedDate, content });
      await reload();
    } else {
      setState(s => ({ ...s, notes: [{ id: 1, date: selectedDate, content }] }));
    }
  };
  return (
    <section className="daily-grid">
      <PerfectOverlay show={perfect} />
      <motion.div className="glass-card hero-card" initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }}>
        <span className="eyebrow">{pretty(selectedDate)}</span>
        <h1>오늘의 루틴</h1>
        <p>체크 한 번마다 보라색 글로우, 파티클, 도넛 카운트업이 연결되는 루틴 관리 화면입니다.</p>
        <ProgressDonut value={pct} />
        <div className="stat-row"><b>{completed}</b><span>완료</span><b>{Math.max(tasks.length - completed, 0)}</b><span>미완료</span></div>
      </motion.div>
      <motion.div className="glass-card task-card" initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: .08 }}>
        <div className="card-header"><div><span className="eyebrow">할 일</span><h2>오늘의 체크리스트</h2></div><Sparkles size={22} /></div>
        <form className="add-task" onSubmit={add}><input value={title} onChange={e => setTitle(e.target.value)} placeholder="새 루틴을 입력하고 Enter" /><button><CirclePlus size={18} />추가</button></form>
        <AnimatePresence mode="popLayout">{tasks.map(task => <TaskRow key={task.id} task={task} onToggle={() => toggle(task)} onDelete={() => remove(task)} />)}</AnimatePresence>
      </motion.div>
      <motion.div className="glass-card notes-card" initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: .14 }}>
        <div className="card-header"><div><span className="eyebrow">메모</span><h2>오늘의 기록</h2></div></div>
        <textarea defaultValue={note} onBlur={e => setNote(e.currentTarget.value)} placeholder="오늘의 자유 메모" />
      </motion.div>
    </section>
  );
}

function WeeklyView({ state, setView, setSelectedDate }: { state: AppState; setView: (v: ViewKey) => void; setSelectedDate: (date: string) => void }) {
  const today = new Date();
  const monday = new Date(today);
  monday.setDate(today.getDate() - ((today.getDay() + 6) % 7));
  const days = Array.from({ length: 7 }, (_, i) => { const d = new Date(monday); d.setDate(monday.getDate() + i); return iso(d); });
  const total = days.flatMap(d => state.tasks.filter(t => t.date === d));
  const done = total.filter(t => t.completed).length;
  return (
    <section className="page-stack">
      <div className="section-title"><h1>주간 플래너</h1><p>{done}/{total.length || 1}개 완료 · 주간 진행률 {Math.round((done / Math.max(total.length, 1)) * 100)}%</p></div>
      <div className="weekly-grid">{days.map((day) => {
        const tasks = state.tasks.filter(t => t.date === day);
        const pct = tasks.length ? tasks.filter(t => t.completed).length / tasks.length * 100 : 0;
        return <motion.button className="glass-card weekly-card" key={day} onClick={() => { sound.transition(); setSelectedDate(day); setView('daily'); }} whileHover={{ y: -7 }}><span className="eyebrow">{dayLabel(day)}</span><h3>{day.slice(5)}</h3><ProgressDonut value={pct} size={120} label="" /><ul>{tasks.slice(0, 4).map(t => <li key={t.id} className={t.completed ? 'mini-done' : ''}>{t.title}</li>)}</ul><ChevronRight size={18} /></motion.button>;
      })}</div>
    </section>
  );
}

function MonthlyHabits({ state, reload, setState }: { state: AppState; reload: () => Promise<void>; setState: React.Dispatch<React.SetStateAction<AppState>> }) {
  const now = new Date();
  const year = now.getFullYear();
  const month = now.getMonth();
  const days = new Date(year, month + 1, 0).getDate();
  const dates = Array.from({ length: days }, (_, i) => formatDateLocal(new Date(year, month, i + 1)));
  const baseRecordFor = (habitId: number, date: string) => state.habitRecords.find(r => r.habit_id === habitId && r.date === date);
  const [demoActive, setDemoActive] = useState(false);
  const [demoStep, setDemoStep] = useState(0);
  const demoSequence = useMemo(() => {
    const habitCount = Math.max(state.habits.length, 1);
    const seededNoise = (value: number) => {
      const raw = Math.sin(value * 12.9898 + 78.233) * 43758.5453;
      return raw - Math.floor(raw);
    };
    const cells = dates.flatMap((date, dayIndex) => state.habits.map((habit, habitIndex) => {
      const seed = (habit.id + 17) * 83492791 + (dayIndex + 3) * 19349663 + (habitIndex + 5) * 73856093;
      const scatter = seededNoise(seed);
      const diagonalAccent = Math.abs((dayIndex % habitCount) - habitIndex) * 0.17;
      const weekAccent = ((dayIndex + habitIndex * 4) % 7) * 0.09;
      const lateMonthLift = dayIndex * 0.018;
      return {
        key: `${habit.id}-${date}`,
        habitId: habit.id,
        date,
        seed,
        order: scatter * 8 + diagonalAccent + weekAccent + lateMonthLift
      };
    }));
    return cells.sort((a, b) => a.order - b.order);
  }, [dates.join('|'), state.habits]);
  const demoVisible = demoStep > 0;
  const demoSet = useMemo(() => new Set(demoSequence.slice(0, demoStep).map(cell => cell.key)), [demoSequence, demoStep]);
  const recentDemoSet = useMemo(() => new Set(demoSequence.slice(Math.max(0, demoStep - 6), demoStep).map(cell => cell.key)), [demoSequence, demoStep]);
  const latestDemoCell = demoVisible ? demoSequence[Math.min(Math.max(demoStep - 1, 0), Math.max(demoSequence.length - 1, 0))] : undefined;
  const demoProgress = Math.min(100, Math.round((demoStep / Math.max(demoSequence.length, 1)) * 100));
  const isDemoCell = (habitId: number, date: string) => demoSet.has(`${habitId}-${date}`);
  const isRecentDemoCell = (habitId: number, date: string) => recentDemoSet.has(`${habitId}-${date}`);
  const isCompleted = (habitId: number, date: string) => demoVisible ? isDemoCell(habitId, date) : !!baseRecordFor(habitId, date)?.completed;
  const completedCells = state.habits.reduce((sum, habit) => sum + dates.filter(d => isCompleted(habit.id, d)).length, 0);
  const totalCells = Math.max(state.habits.length * dates.length, 1);
  const incompleteCells = Math.max(totalCells - completedCells, 0);
  const completionRate = Math.round((completedCells / totalCells) * 100);
  const pieData = [
    { name: '완료', value: completedCells, color: demoVisible ? '#F97316' : '#7C3AED' },
    { name: '미완료', value: incompleteCells, color: demoVisible ? '#FFE4E6' : '#EDE9FE' }
  ];
  const lineData = dates.map((date) => ({
    날짜: Number(date.slice(8)),
    완료수: state.habits.filter(habit => isCompleted(habit.id, date)).length,
    전체습관: state.habits.length,
    최근점등: latestDemoCell?.date === date ? state.habits.filter(habit => isCompleted(habit.id, date)).length : undefined
  }));
  const weekSummary = Array.from({ length: Math.ceil(days / 7) }, (_, index) => {
    const weekDates = dates.slice(index * 7, index * 7 + 7);
    const weekTotal = Math.max(weekDates.length * state.habits.length, 1);
    const weekDone = state.habits.reduce((sum, habit) => sum + weekDates.filter(d => isCompleted(habit.id, d)).length, 0);
    return { week: index + 1, rate: Math.round((weekDone / weekTotal) * 100) };
  });
  const startDemo = () => {
    setDemoStep(0);
    setDemoActive(true);
    sound.add();
    confetti({ particleCount: 80, spread: 80, origin: { x: .5, y: .16 }, colors: ['#F97316', '#EC4899', '#8B5CF6', '#22C55E'] });
  };
  const resetDemo = () => {
    setDemoActive(false);
    setDemoStep(0);
  };
  useEffect(() => {
    if (!demoActive) return;
    if (demoStep >= demoSequence.length) {
      setDemoActive(false);
      sound.perfect();
      confetti({ particleCount: 170, spread: 118, origin: { x: .5, y: .24 }, colors: ['#FACC15', '#F97316', '#EC4899', '#8B5CF6', '#22C55E'] });
      return;
    }
    const current = demoSequence[demoStep];
    const delay = current ? 48 + (Math.abs(current.seed) % 95) : 72;
    const burst = current && Math.abs(current.seed) % 13 === 0 ? 3 : current && Math.abs(current.seed) % 7 === 0 ? 2 : 1;
    const timer = window.setTimeout(() => {
      setDemoStep(step => Math.min(step + burst, demoSequence.length));
    }, delay);
    return () => window.clearTimeout(timer);
  }, [demoActive, demoStep, demoSequence]);
  const toggle = async (habit: Habit, date: string) => {
    if (demoVisible) resetDemo();
    sound.check();
    if (window.routineAPI) {
      await window.routineAPI.toggleHabitRecord({ habit_id: habit.id, date });
      await reload();
    } else {
      setState(s => ({ ...s, habitRecords: [...s.habitRecords.filter(r => !(r.habit_id === habit.id && r.date === date)), { id: Date.now(), habit_id: habit.id, date, completed: baseRecordFor(habit.id, date)?.completed ? 0 : 1 }] }));
    }
  };
  return (
    <section className={`page-stack monthly-reels-stage ${demoActive ? 'demo-running' : ''} ${demoVisible ? 'demo-visible' : ''}`}>
      <motion.div className="reels-demo-hero" initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }}>
        <div className="demo-aurora" />
        <div className="demo-copy">
          <span className="eyebrow"><Sparkles size={14} /> 릴스 촬영 모드</span>
          <h1>월간 루틴이 한 번에 채워지는 시네마틱 데모</h1>
          <p>스마트폰으로 화면을 촬영할 때 체크박스가 예측하기 어려운 순서로 반짝이며 채워지고, 원형 차트와 꺾은선 차트가 같은 진행률로 실시간 반응합니다.</p>
          <div className="demo-progress"><motion.span animate={{ width: `${demoProgress}%` }} transition={{ duration: .25 }} /></div>
        </div>
        <div className="demo-actions">
          <motion.button className="demo-button primary" onClick={startDemo} whileHover={{ scale: 1.04 }} whileTap={{ scale: .96 }}>
            <Wand2 size={18} /> {demoActive ? '데모 진행 중' : demoVisible ? '데모 다시보기' : '데모 버튼'}
          </motion.button>
          {demoVisible && <button className="demo-button ghost" onClick={resetDemo}>실제 데이터 보기</button>}
          <strong>{demoProgress}%</strong>
        </div>
        {demoVisible && <div className="floating-sparkles"><i /><i /><i /><i /></div>}
      </motion.div>
      <div className="section-title"><h1>월간 습관표</h1><p>데모 버튼을 누르면 월간표의 체크박스와 원형·꺾은선 차트가 릴스 촬영용으로 자동 진행됩니다.</p></div>
      <div className="monthly-analytics reels-analytics">
        <motion.div className="glass-card monthly-chart-card pie-pop-card" initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0, scale: demoActive ? [1, 1.025, 1] : 1 }} transition={{ duration: .75, repeat: demoActive ? Infinity : 0 }}>
          <div className="card-header"><div><span className="eyebrow">월간 달성률</span><h2>완료/미완료 원형 차트</h2></div><strong className="chart-kpi">{completionRate}%</strong></div>
          <ResponsiveContainer width="100%" height={260}>
            <PieChart>
              <Pie key={`pie-${completedCells}-${demoStep}`} data={pieData} dataKey="value" nameKey="name" innerRadius={62} outerRadius={92} paddingAngle={4} isAnimationActive animationBegin={0} animationDuration={260}>
                {pieData.map((entry) => <Cell key={entry.name} fill={entry.color} />)}
              </Pie>
              <Tooltip formatter={(value) => [`${value}칸`, '체크 수']} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </motion.div>
        <motion.div className="glass-card monthly-chart-card line-sweep-card" initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0, boxShadow: demoActive ? ['0 18px 50px rgba(124,58,237,.14)', '0 24px 70px rgba(236,72,153,.26)', '0 18px 50px rgba(124,58,237,.14)'] : '0 18px 50px rgba(124,58,237,.14)' }} transition={{ delay: .08, duration: 1.2, repeat: demoActive ? Infinity : 0 }}>
          <div className="card-header"><div><span className="eyebrow">일별 흐름</span><h2>체크 수 꺾은선 차트</h2></div><div className="chart-live-badge"><Activity size={16} /> {demoVisible && latestDemoCell ? `${Number(latestDemoCell.date.slice(8))}일 반응` : '실시간'}</div></div>
          <ResponsiveContainer width="100%" height={260}>
            <LineChart data={lineData} margin={{ top: 10, right: 14, bottom: 0, left: -18 }}>
              <CartesianGrid stroke="rgba(124,58,237,.13)" />
              <XAxis dataKey="날짜" />
              <YAxis allowDecimals={false} domain={[0, Math.max(state.habits.length, 1)]} />
              <Tooltip formatter={(value, name) => [`${value}개`, name]} labelFormatter={(label) => `${label}일`} />
              <Line key={`demo-line-${demoVisible ? demoStep : 'real'}`} type="monotone" dataKey="완료수" name="완료 수" stroke={demoVisible ? '#F97316' : '#7C3AED'} strokeWidth={4} dot={{ r: 4, fill: demoVisible ? '#FDBA74' : '#A78BFA' }} activeDot={{ r: 7 }} isAnimationActive animationBegin={0} animationDuration={240} />
              <Line type="monotone" dataKey="전체습관" name="전체 습관" stroke="#C4B5FD" strokeDasharray="6 6" strokeWidth={2} dot={false} isAnimationActive={false} />
              {demoVisible && <Line key={`recent-line-${demoStep}`} type="monotone" dataKey="최근점등" name="최근 반응" stroke="#22C55E" strokeWidth={0} dot={{ r: 8, fill: '#22C55E', stroke: '#FFFFFF', strokeWidth: 3 }} activeDot={{ r: 9 }} isAnimationActive animationDuration={180} />}
            </LineChart>
          </ResponsiveContainer>
        </motion.div>
      </div>
      <div className="glass-card monthly-table reels-monthly-table">
        <div className="table-shine" />
        <div className="habit-grid header" style={{ gridTemplateColumns: `190px repeat(${dates.length}, 30px) 54px` }}><strong>습관</strong>{dates.map(d => <span key={d}>{Number(d.slice(8))}<small>{dayInitial(d)}</small></span>)}<strong>달성률</strong></div>
        {state.habits.map((habit) => {
          const done = dates.filter(d => isCompleted(habit.id, d)).length;
          return <div className="habit-grid" key={habit.id} style={{ gridTemplateColumns: `190px repeat(${dates.length}, 30px) 54px` }}><strong style={{ color: habit.color }}>{habit.name}<small><Flame size={12} /> {habit.streak_count}일 연속</small></strong>{dates.map((d) => { const checked = isCompleted(habit.id, d); const demoLit = demoVisible && isDemoCell(habit.id, d); const demoRecent = demoVisible && isRecentDemoCell(habit.id, d); return <motion.button key={d} className={`habit-cell ${checked ? 'checked' : ''} ${demoLit ? 'demo-lit' : ''} ${demoRecent ? 'demo-newest' : ''}`} onClick={() => toggle(habit, d)} whileTap={{ scale: .9 }} whileHover={{ scale: 1.08 }} animate={demoRecent ? { scale: [1, 1.42, .96, 1], rotate: [0, -10, 7, 0] } : { scale: 1, rotate: 0 }} transition={{ duration: .38, ease: 'easeOut' }} aria-label={`${habit.name} ${Number(d.slice(8))}일 체크박스`} aria-pressed={checked}><Check size={12} /></motion.button>; })}<b>{Math.round(done / dates.length * 100)}%</b></div>;
        })}
        <div className="week-summary">{weekSummary.map(item => <span key={item.week}>{item.week}주차<b>{item.rate}%</b></span>)}</div>
      </div>
    </section>
  );
}
function Analytics({ state }: { state: AppState }) {
  const currentMonth = iso().slice(0, 7);
  const habitData = state.habits.map(h => {
    const actual = state.habitRecords.filter(r => r.habit_id === h.id && monthKey(r.date) === currentMonth && r.completed).length;
    return { 습관: h.name.split(' ')[0], 목표: h.goal_per_month, 실제: actual };
  });
  const trend = Array.from({ length: 6 }, (_, i) => {
    const d = new Date();
    d.setMonth(d.getMonth() - (5 - i));
    const key = formatDateLocal(d).slice(0, 7);
    return { 월: `${key.slice(5)}월`, 완료: state.habitRecords.filter(r => monthKey(r.date) === key && r.completed).length };
  });
  return (
    <section className="analytics-grid">
      <div className="glass-card chart-card"><div className="card-header"><div><span className="eyebrow">목표 대비 실제</span><h2>월간 성과</h2></div></div><ResponsiveContainer width="100%" height={310}><BarChart data={habitData}><CartesianGrid stroke="rgba(124,58,237,.13)"/><XAxis dataKey="습관"/><YAxis/><Tooltip/><Legend/><Bar dataKey="목표" fill="#C4B5FD" radius={[8,8,0,0]}/><Bar dataKey="실제" fill="#7C3AED" radius={[8,8,0,0]}/></BarChart></ResponsiveContainer></div>
      <div className="glass-card chart-card"><div className="card-header"><div><span className="eyebrow">흐름</span><h2>월별 추세</h2></div><Activity /></div><ResponsiveContainer width="100%" height={310}><LineChart data={trend}><CartesianGrid stroke="rgba(124,58,237,.13)"/><XAxis dataKey="월"/><YAxis/><Tooltip/><Line type="monotone" dataKey="완료" stroke="#7C3AED" strokeWidth={4} dot={{ r: 5, fill: '#A78BFA' }}/></LineChart></ResponsiveContainer></div>
      <div className="glass-card metric-card"><Trophy /><strong>{state.habitRecords.filter(r => r.completed).length}</strong><span>누적 완료 습관</span></div>
    </section>
  );
}

function SettingsView({ state, reload, setState }: { state: AppState; reload: () => Promise<void>; setState: React.Dispatch<React.SetStateAction<AppState>> }) {
  const [backup, setBackup] = useState('');
  const update = async (patch: Partial<SettingsState>) => {
    const next = { ...state.settings, ...patch };
    sound.configure(next);
    if (window.routineAPI) {
      await window.routineAPI.updateSettings(patch);
      await reload();
    } else {
      setState(s => ({ ...s, settings: next }));
    }
  };
  const exportData = async () => setBackup(JSON.stringify(window.routineAPI ? await window.routineAPI.exportData() : state, null, 2));
  const importData = async () => {
    if (!backup.trim()) return;
    const payload = JSON.parse(backup);
    if (window.routineAPI) {
      await window.routineAPI.importData(payload);
      await reload();
    } else {
      setState(payload);
    }
  };
  const intensityLabel: Record<EffectIntensity, string> = { subtle: '은은하게', normal: '기본', cinematic: '시네마틱' };
  return (
    <section className="settings-grid">
      <div className="glass-card"><span className="eyebrow">화면</span><h2>표시 모드</h2><div className="segmented"><button className={state.settings.theme === 'light' ? 'active' : ''} onClick={() => update({ theme: 'light' })}><Sun size={16}/> 라이트</button><button className={state.settings.theme === 'dark' ? 'active' : ''} onClick={() => update({ theme: 'dark' })}><Moon size={16}/> 다크</button><button className={state.settings.theme === 'system' ? 'active' : ''} onClick={() => update({ theme: 'system' })}>시스템</button></div></div>
      <div className="glass-card"><span className="eyebrow">오디오</span><h2>사운드 설정</h2><label className="toggle-row"><Music2/> 효과음 <input type="checkbox" checked={state.settings.sound} onChange={e => update({ sound: e.target.checked })}/></label></div>
      <div className="glass-card"><span className="eyebrow">효과</span><h2>시각 효과 강도</h2><div className="segmented">{(['subtle','normal','cinematic'] as EffectIntensity[]).map(v => <button key={v} className={state.settings.effectIntensity === v ? 'active' : ''} onClick={() => update({ effectIntensity: v, cinematicMode: v === 'cinematic' })}><Wand2 size={16}/>{intensityLabel[v]}</button>)}</div><p className="hint">Cmd+Shift+R 데모 모드는 촬영용 자동 체크/언체크 시퀀스로 확장할 수 있도록 구조를 마련했습니다.</p></div>
      <div className="glass-card backup-card"><span className="eyebrow">데이터</span><h2>JSON 백업 / 복원</h2><div className="backup-actions"><button onClick={exportData}><Download size={16}/>내보내기</button><button onClick={importData}><Upload size={16}/>가져오기</button></div><textarea value={backup} onChange={e => setBackup(e.target.value)} placeholder="내보내기를 누르면 JSON 백업이 표시됩니다." /></div>
    </section>
  );
}

function Sidebar({ view, setView, state }: { view: ViewKey; setView: (view: ViewKey) => void; state: AppState }) {
  const items: { key: ViewKey; label: string; icon: React.ReactNode }[] = [
    { key: 'daily', label: '일간', icon: <LayoutDashboard size={18}/> },
    { key: 'weekly', label: '주간', icon: <CalendarDays size={18}/> },
    { key: 'monthly', label: '월간', icon: <Check size={18}/> },
    { key: 'analytics', label: '분석', icon: <Activity size={18}/> },
    { key: 'settings', label: '설정', icon: <Settings size={18}/> }
  ];
  const todayTasks = state.tasks.filter(t => t.date === iso());
  const pct = todayTasks.length ? todayTasks.filter(t => t.completed).length / todayTasks.length * 100 : 0;
  return <aside className="sidebar"><div className="brand"><div className="logo"><Check size={23}/></div><div><strong>루틴</strong><span>트래커</span></div></div><nav>{items.map(item => <button key={item.key} className={view === item.key ? 'active' : ''} onMouseEnter={() => sound.hover()} onClick={() => { sound.transition(); setView(item.key); }}>{item.icon}<span>{item.label}</span></button>)}</nav><div className="sidebar-streak"><Flame size={19}/><span>오늘 진행률</span><strong>{Math.round(pct)}%</strong><ProgressDonut value={pct} size={92} label="" /></div></aside>;
}

function App() {
  const { state, setState, reload } = useRoutineState();
  const [view, setView] = useState<ViewKey>('daily');
  const [selectedDate, setSelectedDate] = useState(iso());
  const mainRef = useRef<HTMLElement>(null);
  useEffect(() => {
    sound.configure(state.settings);
    document.documentElement.dataset.theme = state.settings.theme === 'system' ? (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light') : state.settings.theme;
    document.documentElement.dataset.effects = state.settings.effectIntensity;
  }, [state.settings]);
  useEffect(() => {
    const handler = (event: KeyboardEvent) => {
      if ((event.metaKey || event.ctrlKey) && event.key === 'd') {
        void (window.routineAPI?.updateSettings({ theme: document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark' }).then(reload));
      }
      if ((event.metaKey || event.ctrlKey) && event.shiftKey && event.key.toLowerCase() === 'r') {
        void window.routineAPI?.notifyDemo();
        confetti({ particleCount: 120, spread: 100, colors: ['#7C3AED','#A78BFA','#C4B5FD'] });
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [reload]);
  const title = { daily: '일간 보기', weekly: '주간 플래너', monthly: '월간 습관표', analytics: '분석', settings: '설정' }[view];
  return (
    <div className="app-shell">
      <div className="ambient one"/><div className="ambient two"/><div className="ambient three"/>
      <Sidebar view={view} setView={setView} state={state}/>
      <section className="content-shell">
        <header className="topbar"><div><span className="eyebrow">{pretty(selectedDate)}</span><h1>{title}</h1></div><div className="top-actions"><button aria-label="테마 전환" onClick={() => setState(s => ({ ...s, settings: { ...s.settings, theme: document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark' } }))}><Moon size={17}/></button><button aria-label="효과음 전환" onClick={() => { const next = !state.settings.sound; void (window.routineAPI?.updateSettings({ sound: next }).then(reload)); setState(s => ({ ...s, settings: { ...s.settings, sound: next } })); }}><Music2 size={17}/></button></div></header>
        <main ref={mainRef} className="main-panel"><AnimatePresence mode="wait"><motion.div key={view} initial={{ opacity: 0, x: 28, filter: 'blur(8px)' }} animate={{ opacity: 1, x: 0, filter: 'blur(0px)' }} exit={{ opacity: 0, x: -26, filter: 'blur(8px)' }} transition={{ duration: .32, ease: 'easeOut' }}>{view === 'daily' && <DailyView state={state} selectedDate={selectedDate} reload={reload} setState={setState}/>} {view === 'weekly' && <WeeklyView state={state} setView={setView} setSelectedDate={setSelectedDate}/>} {view === 'monthly' && <MonthlyHabits state={state} reload={reload} setState={setState}/>} {view === 'analytics' && <Analytics state={state}/>} {view === 'settings' && <SettingsView state={state} reload={reload} setState={setState}/>}</motion.div></AnimatePresence></main>
      </section>
    </div>
  );
}

createRoot(document.getElementById('root')!).render(<React.StrictMode><App /></React.StrictMode>);
