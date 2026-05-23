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
