<template>
    <div id="new-answer-assessment">
        <b-container class="bv-example-row">
            <b-row>
                <!-- lewa kolumna -->
                <b-col>
                    <div class="answer-data">
                        <p class="text-muted">
                            <strong>{{ answer.author }} </strong> &#8901; {{ answer.created_at }}
                        </p>
                        <p>Maksymalna liczba punktów: {{ answer.max_score }}</p>
                    </div>
                    <p>Plik: {{ answer.answer_file }}</p>
                    <div class="img-answer">
                        <a v-bind:href="answer.answer_file">
                            <b-img class="img-full" v-bind:src="answer.answer_file" fluid-grow alt="Fluid image"></b-img>
                        </a>
                    </div>
                    <div v-if="userHasAnswered">
                        <p class="documentAssessment-added"> Już dodałeś ocenę do tego zadania</p>
                    </div>
                    <div v-else-if="!showForm">
                        <button
                        class="btn tbn-sm btn-success"
                        @click="showForm = true"
                        >Oceń zadanie
                        </button>
                    </div>
                    <div v-else>
                        <!-- dodawanie oceny pojedynczego zadania -->
                        <div class="add-answer-assessment">
                                <form v-if="showForm" @submit.prevent="addAnswerAssessment">
                                    <div>
                                        <p>Liczba punktów <input v-model.number="scores" type="number"></p>
                                    </div>
                                    <div class="card-block">
                                        <textarea
                                        v-model="newAnswerAssessmentBody"
                                        class="form-control"
                                        placeholder="Opisz wybrane zadanie"
                                        rows="5"
                                        ></textarea>
                                    </div>
                                    <br>
                                    <div class="card-footer px-3">
                                        <button type="submit" class="btn btn-sm btn-success">Oceń zadanie</button>
                                    </div>
                                    <router-link :to="{ name: 'document', params: {document_id: document_id } }" class="btn btn-sm btn-danger">Wróć do dokumentu</router-link>
                                </form>
                        </div>
                    </div>
                </b-col>

                <!-- prawa kolumna -->
                <b-col>        
                    <!-- Wyświetlanie ocen odpowiedzi -->
                    <div class="container">
                        <AnswerAssessmentComponent 
                            v-for="(answerAssessment, index) in answerAssessments"
                            :answerAssessment="answerAssessment"
                            :answer_id="answer_id"
                            :document_id="document_id"
                            :v-key="index"
                        />
                    </div>

                    <!-- ładowanie kolejnych odpwoiedzi -->
                    <div class="my-4">
                        <p v-show="loadingAnswerAssessments">...loading...</p>
                        <button
                        v-show="nextAnswerAssessments"
                        @click="getAnswerAssessments"
                        class="btn btn-sm btn-outline-info"
                        >Więcej ocen zadania
                        </button>
                    </div>
                    <!-- end loading more data button section -->
                </b-col>
            </b-row>
        </b-container>
    </div>
</template>

<script>
import axios from 'axios';

import AnswerAssessmentComponent from '@/components/AnswerAssessmentComponent.vue'
import { CSRF_TOKEN } from "@/common/csrf_token.js";
export default {
    name: "AnswerAssessment",
    props: {
        answer_id: {
            type: String | Number,
            required: true
        },
        document_id: {
          type: String | Number,
          required: true
        }
    },
    data(){
        return{
            answer: {},
            answerAssessments: [],
            scores: null, 
            newAnswerAssessmentBody: null,
            loadingAnswerAssessments: false,
            nextAnswerAssessments: null,
            error: null,
            userHasAnswered: false,
            showForm: false,
            requestUser: null
        }
    },
    components: {
        AnswerAssessmentComponent
    },
    methods:{
        setRequestUser(){
            this.requestUser = window.localStorage.getItem("username");
            console.log(this.requestUser);
        },
        getAnswer(){
            let endpoint = `/api/documents/${this.document_id}/answer/${this.answer_id}/`;
            axios.get(endpoint)
                .then(response => {
                    if(response){
                        this.answer = response.data;
                        this.userHasAnswered = response.data.user_has_answered;
                        console.log("this.userHasAnswered: ", this.userHasAnswered)
                    }else{
                        this.answer = null;
                        // this.setPageTitle("404 - Page Not Found");
                }
            })
        },
        
        getAnswerAssessments(){
            let endpoint = `/api/documents/${this.document_id}/answer/${this.answer_id}/answerassessments/`;
            if (this.nextAnswerAssessments){
                endpoint = this.nextAnswerAssessments;
            }
            this.loadingAnswerAssessments = true;

            let vm = this;
            axios.get(endpoint)
                .then(response => {
                    if(response){
                        this.answerAssessments.push(...response.data.results);
                        this.loadingAnswerAssessments = false;
                        if (response.data.next) { //url from django REST for next data (pagination)
                            this.nextAnswerAssessments = response.data.next;
                        }else{ //if no addditional data exists
                            this.nextAnswerAssessments = null;
                        }
                    }
            })
        },

        addAnswerAssessment(){ //TODO: jedna opinia na jednego użytkownika
            //dodawanie oceny pojedynczego zadania
            let endpoint = `/api/documents/${this.document_id}/answer/${this.answer_id}/answerassessment/`;
            
            let newAnswerAssessmentBody = new FormData();
            if (this.newAnswerAssessmentBody){
                //notatka może być pusta
                newAnswerAssessmentBody.set("note",this.newAnswerAssessmentBody)
            }
            if (this.scores){
                // punkty nie mogą być puste!
                newAnswerAssessmentBody.set("scores",this.scores)

                axios.defaults.headers.common = {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFTOKEN': CSRF_TOKEN
                };

                let vm = this;
                axios({
                    method: 'post',
                    url: endpoint,
                    withCredentials: true,
                    data: newAnswerAssessmentBody
                    })
                    .then(function (response) {
                        vm.answerAssessments.unshift(response.data); //dodawanie obiektu na sam poczatek listy
                        vm.userHasAnswered = true;
                    })
                    .catch(function (response) {
                        console.log(response);
                    });
            }
        }
    },
    created(){
        this.getAnswer();
        this.getAnswerAssessments();
        this.setRequestUser();    
    }
}
</script>

<style scoped>
.img-answer{
    max-width: 400px;
    height: auto;
}
</style>