import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
export default defineConfig({
 site:'https://cjgogo27.github.io', base:'/Infra',
 integrations:[starlight({
  title:{'zh-CN':'听懂 Infra',en:'Infra, Explained'},
  description:'从零理解大模型与具身智能的训练、推理和部署',
  locales:{root:{label:'简体中文',lang:'zh-CN'},en:{label:'English',lang:'en'}},
  social:[{icon:'github',label:'GitHub',href:'https://github.com/cjgogo27/Infra'}],
  sidebar:[
   {label:'从这里开始',translations:{en:'Start here'},items:[{autogenerate:{directory:'guides'}}]},
   {label:'一、把系统串起来',translations:{en:'1. Connect the system'},items:[{autogenerate:{directory:'01-foundations'}}]},
   {label:'二、让一次训练跑对',translations:{en:'2. Get training right'},items:[{autogenerate:{directory:'02-training'}}]},
   {label:'三、让多张卡协作',translations:{en:'3. Coordinate GPUs'},items:[{autogenerate:{directory:'03-distributed'}}]},
   {label:'四、找出真正的瓶颈',translations:{en:'4. Find the bottleneck'},items:[{autogenerate:{directory:'04-performance'}}]},
   {label:'五、从模型到服务',translations:{en:'5. From models to services'},items:[{autogenerate:{directory:'05-inference'}}]},
   {label:'六、走进机器人闭环',translations:{en:'6. Close the robot loop'},items:[{autogenerate:{directory:'06-embodied'}}]},
   {label:'动手实验',translations:{en:'Hands-on labs'},items:[{autogenerate:{directory:'labs'}}]},
   {label:'附录与面试',translations:{en:'Appendices and interviews'},items:[{autogenerate:{directory:'appendix'}}]}
  ],
  customCss:['./src/styles/custom.css'],
  editLink:{baseUrl:'https://github.com/cjgogo27/Infra/edit/main/'},
  tableOfContents:{minHeadingLevel:2,maxHeadingLevel:3}
 })]
});
