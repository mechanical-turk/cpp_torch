from pathlib import Path
p=Path('build.py');s=p.read_text()
s=s.replace('# Animation keys are authored on twos', 'PAD=577;LIFT=601;CROSS_START=621;CROSS_END=661;LAND=685;RESULT=721;END=1008\n# Animation keys are authored on twos')
a=s.index('counts=[0,0];previous_active=');b=s.index(' for row in [code_header',a)
s=s[:a]+'''# One ordered request/ownership/transfer cycle per four seconds.
# Bubble lifetimes are independent of the current owner and scene boundaries.
writes=[[],[]];events=[]
for cycle in range(6):
 start=1+cycle*96;requester=1-cycle%2
 writes[requester].append(start+74)
 events.append({'requester':requester,'pulse_start':start,'pulse_arrival':start+24,'ownership_change':start+28,'transfer_start':start+36,'transfer_end':start+72,'write':start+74,'bubble_end':start+108})
for i in range(2):
 base=LAND+8*i
 for t in range(base+26,END+1,72):writes[i].append(t)
for f in range(1,END+1,2):
 moving=LIFT<=f<LAND;settled=f>=LAND
 if f<LIFT:bx=-1.6;bz=.30
 elif f<CROSS_START:bx=-1.6;bz=.30+1.20*smooth((f-LIFT)/20)
 elif f<CROSS_END:bx=-1.6+3.2*smooth((f-CROSS_START)/40);bz=1.50+.13*math.sin(math.pi*(f-CROSS_START)/40)
 elif f<LAND:bx=1.6;bz=.30+1.20*(1-smooth((f-CROSS_END)/24))
 else:bx=1.6;bz=.30
 dx=0;owner=0;requester=None;travel=[False,False];packet=[0,0]
 if f<PAD:
  cycle=(f-1)//96;phase=(f-1)%96;requester=1-cycle%2
  owner=requester if phase>=28 else 1-requester
  old_dx=0 if requester==1 else 5;new_dx=5-old_dx
  dx=old_dx+(new_dx-old_dx)*smooth((phase-36)/36)
  travel[requester]=phase<=24;packet[requester]=smooth(phase/24)
 elif settled:
  for i in range(2):
   base=LAND+8*i;phase=(f-base)%72
   travel[i]=f>=base and phase<=24;packet[i]=smooth(phase/24)
 counts=[sum(t<=f for t in times) for times in writes]
 ages=[f-max([t for t in times if t<=f],default=-1000) for times in writes]
 active=[0<=age<34 for age in ages]
 key(tray,'location',(-2.5+dx,-3.2,0),f)
 key(ca,'location',(-3.4+dx,-3.2,.30),f);key(cb,'location',(bx+dx,-3.2,bz),f)
 for i,g in enumerate([ca,cb]):
  press=1-.02*(1-smooth(ages[i]/8)) if 0<=ages[i]<8 else 1
  key(g,'scale',(.66,.66,.70*press),f)
 for o in [tray2]+list(tray2.children):vis(o,f>=PAD,f)
 pb.inputs['Base Color'].default_value=colors[owner];pb.inputs['Base Color'].keyframe_insert(data_path='default_value',frame=f)
 for node,part in owned_nodes:
  palette=['008F88','2558BE'] if part=='shell' else ['073E3F','132958'];node.inputs['Base Color'].default_value=(*lin(palette[owner]),1);node.inputs['Base Color'].keyframe_insert(data_path='default_value',frame=f)
 for i in range(2):
  start=Vector((-2.5 if i==0 else 2.5,.75,.84));end=Vector(((-3.4 if i==0 else bx)+dx,-2.27,1.06 if i==0 else bz+.76))
  for j,o in enumerate(paths[i]):
   key(o,'location',start.lerp(end,j/7),f);key(o,'rotation_euler',Vector((0,1,0)).rotation_difference((end-start).normalized()).to_euler(),f);vis(o,not moving,f)
  key(beads[i],'location',start.lerp(end,packet[i])+Vector((0,-.04,.04)),f);vis(beads[i],travel[i],f)
  u=max(0,min(1,ages[i]/34));bubble=increments[i]
  strength=.04+.12*(1-smooth(ages[i]/8)) if 0<=ages[i]<8 else .04
  face_nodes[i].inputs['Emission Strength'].default_value=strength;face_nodes[i].inputs['Emission Strength'].keyframe_insert(data_path='default_value',frame=f)
  key(bubble,'location',((-3.4 if i==0 else bx)+dx,-3.25,2.60+1.50*smooth(u)),f)
  envelope=min(1,.75+u*3)*(1-.15*smooth((u-.8)/.2));key(bubble,'scale',(envelope,)*3,f)
  for o in bubble.children:vis(o,active[i],f)
  for value,digit in enumerate(counter_digits[i]):
   vis(digit,value==counts[i],f);bump=1+.12*(1-smooth(ages[i]/8)) if 0<=ages[i]<8 else 1;key(digit,'scale',(bump,)*3,f)
''' +s[b:]
# Shift unchanged code/result choreography by 264 frames.
a=s.index(' for row in [code_header');b=s.index("s.render.engine='CYCLES'",a)
block=s[a:b]
import re
mapping={337:601,345:609,351:615,359:623,413:677,431:695,457:721,479:743,481:745,721:1009}
block=re.sub(r'\b(?:337|345|351|359|413|431|457|479|481|721)\b',lambda m:str(mapping[int(m.group())]),block)
# A replaced range stop is END+1; result threshold remains 721.
s=s[:a]+block+s[b:]
s=s.replace('s.frame_end=720','s.frame_end=END')
s=s.replace("clips=[('01-crowded-opening',1,48),('02-shared-cache-line',49,144),('03-write-ownership',145,312),('04-add-padding',313,456),('05-benchmark-result',457,528),('06-discussion-hold',529,720)]", "clips=[('01-crowded-opening',1,192),('02-shared-cache-line',193,384),('03-write-ownership',385,576),('04-add-padding',577,720),('05-benchmark-result',721,816),('06-discussion-hold',817,1008)]")
s=s.replace('for f in range(1,721):','for f in range(1,END+1):')
s=s.replace("'revision':6", "'revision':7").replace("'pulse_travel_seconds':22/24,'increment_hold_seconds':20/24", "'pulse_travel_seconds':1.0,'increment_hold_seconds':34/24,'handoff_seconds':4.0,'contention_events':events,'write_events':writes,'activity_continues_through_result':True")
s=s.replace('for f in [31,41,385,500]:','for f in [25,29,55,91,649,799]:')
p.write_text(s)
