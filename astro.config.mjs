import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
export default defineConfig({
 site:'https://cjgogo27.github.io', base:'/Infra',
 integrations:[starlight({
  title:'听懂 Infra',
  description:'从零理解大模型与具身智能的训练、推理和部署',
  locales:{root:{label:'简体中文',lang:'zh-CN'}},
  social:[{icon:'github',label:'GitHub',href:'https://github.com/cjgogo27/Infra'}],
  sidebar:[
   {label:'从这里开始',items:[{autogenerate:{directory:'guides'}}]},
   {label:'一、把系统串起来',items:[{autogenerate:{directory:'01-foundations'}}]},
   {label:'二、让一次训练跑对',items:[{autogenerate:{directory:'02-training'}}]},
   {label:'三、让多张卡协作',items:[{autogenerate:{directory:'03-distributed'}}]},
   {label:'四、找出真正的瓶颈',items:[{autogenerate:{directory:'04-performance'}}]},
   {label:'五、从模型到服务',items:[{autogenerate:{directory:'05-inference'}}]},
   {label:'六、走进机器人闭环',items:[{autogenerate:{directory:'06-embodied'}}]},
   {label:'动手实验',items:[{autogenerate:{directory:'labs'}}]},
   {label:'附录与面试',items:[{autogenerate:{directory:'appendix'}}]}
  ],
  customCss:['./src/styles/custom.css'],
  editLink:{baseUrl:'https://github.com/cjgogo27/Infra/edit/main/'},
  tableOfContents:{minHeadingLevel:2,maxHeadingLevel:3}
 })]
});
