<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('user_highlights', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->onDelete('cascade');
            $table->string('study_space_name')->default('default');
            $table->string('key')->index();
            $table->integer('book_number');
            $table->integer('chapter');
            $table->integer('verse');
            $table->text('content');
            $table->timestamps();
            
            $table->unique(['user_id', 'study_space_name', 'key']);
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('user_highlights');
    }
};
