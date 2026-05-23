from pathlib import Path

path = Path('/home/ubuntu/routine-tracker/src/renderer/main.tsx')
text = path.read_text()
start = text.index('function MonthlyHabits(')
end = text.index('\nfunction Analytics(', start)
new = r'''function MonthlyHabits({ state, reload, setState }: { state: AppState; reload: () => Promise<void>; setState: React.Dispatch<React.SetStateAction<AppState>> }) {
  const now = new Date();
  const year = now.getFullYear();
  const month = now.getMonth();
  const days = new Date(year, month + 1, 0).getDate();
  const dates = Array.from({ length: days }, (_, i) => formatDateLocal(new Date(year, month, i + 1)));
  const baseRecordFor = (habitId: number, date: string) => state.habitRecords.find(r => r.habit_id === habitId && r.date === date);
  const [demoActive, setDemoActive] = useState(false);
  const [demoStep, setDemoStep] = useState(0);
  const demoSequence = useMemo(() => {
    const cells = dates.flatMap((date, dayIndex) => state.habits.map((habit, habitIndex) => ({
      key: `${habit.id}-${date}`,
      habitId: habit.id,
      date,
      rank: dayIndex * Math.max(state.habits.length, 1) + habitIndex
    })));
    return cells.filter((cell, index) => index % 5 !== 1 || cell.rank < state.habits.length * 4).slice(0, Math.min(cells.length, 120));
  }, [dates.join('|'), state.habits]);
  const demoVisible = demoStep > 0;
  const demoSet = useMemo(() => new Set(demoSequence.slice(0, demoStep).map(cell => cell.key)), [demoSequence, demoStep]);
  const demoProgress = Math.min(100, Math.round((demoStep / Math.max(demoSequence.length, 1)) * 100));
  const isDemoCell = (habitId: number, date: string) => demoSet.has(`${habitId}-${date}`);
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
    전체습관: state.habits.length
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
      confetti({ particleCount: 150, spread: 110, origin: { x: .5, y: .24 }, colors: ['#FACC15', '#F97316', '#EC4899', '#8B5CF6', '#22C55E'] });
      return;
    }
    const timer = window.setTimeout(() => {
      setDemoStep(step => Math.min(step + Math.max(2, Math.ceil(demoSequence.length / 48)), demoSequence.length));
    }, 85);
    return () => window.clearTimeout(timer);
  }, [demoActive, demoStep, demoSequence.length]);
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
          <p>스마트폰으로 화면을 촬영할 때 체크박스, 원형 차트, 꺾은선 차트가 동시에 살아 움직이도록 연출했습니다.</p>
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
        <motion.div className="glass-card monthly-chart-card pie-pop-card" initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0, scale: demoActive ? [1, 1.02, 1] : 1 }} transition={{ duration: .8, repeat: demoActive ? Infinity : 0 }}>
          <div className="card-header"><div><span className="eyebrow">월간 달성률</span><h2>완료/미완료 원형 차트</h2></div><strong className="chart-kpi">{completionRate}%</strong></div>
          <ResponsiveContainer width="100%" height={260}>
            <PieChart>
              <Pie data={pieData} dataKey="value" nameKey="name" innerRadius={62} outerRadius={92} paddingAngle={4} animationDuration={650}>
                {pieData.map((entry) => <Cell key={entry.name} fill={entry.color} />)}
              </Pie>
              <Tooltip formatter={(value) => [`${value}칸`, '체크 수']} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </motion.div>
        <motion.div className="glass-card monthly-chart-card line-sweep-card" initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0, boxShadow: demoActive ? ['0 18px 50px rgba(124,58,237,.14)', '0 24px 70px rgba(236,72,153,.26)', '0 18px 50px rgba(124,58,237,.14)'] : '0 18px 50px rgba(124,58,237,.14)' }} transition={{ delay: .08, duration: 1.2, repeat: demoActive ? Infinity : 0 }}>
          <div className="card-header"><div><span className="eyebrow">일별 흐름</span><h2>체크 수 꺾은선 차트</h2></div><Activity /></div>
          <ResponsiveContainer width="100%" height={260}>
            <LineChart data={lineData} margin={{ top: 10, right: 14, bottom: 0, left: -18 }}>
              <CartesianGrid stroke="rgba(124,58,237,.13)" />
              <XAxis dataKey="날짜" />
              <YAxis allowDecimals={false} domain={[0, Math.max(state.habits.length, 1)]} />
              <Tooltip formatter={(value, name) => [`${value}개`, name]} labelFormatter={(label) => `${label}일`} />
              <Line type="monotone" dataKey="완료수" name="완료 수" stroke={demoVisible ? '#F97316' : '#7C3AED'} strokeWidth={4} dot={{ r: 4, fill: demoVisible ? '#FDBA74' : '#A78BFA' }} activeDot={{ r: 7 }} animationDuration={700} />
              <Line type="monotone" dataKey="전체습관" name="전체 습관" stroke="#C4B5FD" strokeDasharray="6 6" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </motion.div>
      </div>
      <div className="glass-card monthly-table reels-monthly-table">
        <div className="table-shine" />
        <div className="habit-grid header" style={{ gridTemplateColumns: `190px repeat(${dates.length}, 30px) 54px` }}><strong>습관</strong>{dates.map(d => <span key={d}>{Number(d.slice(8))}<small>{dayInitial(d)}</small></span>)}<strong>달성률</strong></div>
        {state.habits.map((habit, habitIndex) => {
          const done = dates.filter(d => isCompleted(habit.id, d)).length;
          return <div className="habit-grid" key={habit.id} style={{ gridTemplateColumns: `190px repeat(${dates.length}, 30px) 54px` }}><strong style={{ color: habit.color }}>{habit.name}<small><Flame size={12} /> {habit.streak_count}일 연속</small></strong>{dates.map((d, dateIndex) => { const checked = isCompleted(habit.id, d); const demoLit = demoVisible && isDemoCell(habit.id, d); return <motion.button key={d} className={`habit-cell ${checked ? 'checked' : ''} ${demoLit ? 'demo-lit' : ''}`} onClick={() => toggle(habit, d)} whileTap={{ scale: .9 }} whileHover={{ scale: 1.08 }} animate={demoLit ? { scale: [1, 1.34, 1], rotate: [0, -8, 8, 0] } : { scale: 1, rotate: 0 }} transition={{ delay: demoActive ? Math.min((habitIndex + dateIndex) * .006, .18) : 0, duration: .35 }} aria-label={`${habit.name} ${Number(d.slice(8))}일 체크박스`} aria-pressed={checked}><Check size={12} /></motion.button>; })}<b>{Math.round(done / dates.length * 100)}%</b></div>;
        })}
        <div className="week-summary">{weekSummary.map(item => <span key={item.week}>{item.week}주차<b>{item.rate}%</b></span>)}</div>
      </div>
    </section>
  );
}'''
path.write_text(text[:start] + new + text[end:])
print('updated monthly reels demo')
